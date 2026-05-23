from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import re
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# LOAD MODELS
# ==========================
category_model = joblib.load("category_model.pkl")
severity_model = joblib.load("severity_model.pkl")
rootcause_model = joblib.load("rootcause_model.pkl")

tfidf_category = joblib.load("tfidf.pkl")
tfidf_severity = joblib.load("tfidf_severity.pkl")
tfidf_rootcause = joblib.load("tfidf_rootcause.pkl")

rootcause_encoder = joblib.load(
    "rootcause_encoder.pkl"
)

# dataset for fix mapping
df = pd.read_csv("devops_logs_5000.csv")

fix_mapping = (
    df.groupby("root_cause")
    ["suggested_fix"]
    .first()
    .to_dict()
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["logfile"]

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    with open(path, "r",
              encoding="utf-8") as f:
        logs = f.readlines()

    # ==========================
    # CLEAN LOGS
    # ==========================
    clean_logs = []

    for line in logs:

        line = line.strip()

        if "INFO" in line or "DEBUG" in line:
            continue

        line = re.sub(
            r'[^a-zA-Z0-9 ]',
            ' ',
            line
        )

        line = line.lower()

        if len(line) > 5:
            clean_logs.append(line)

    # ==========================
    # INCIDENT GROUPING
    # ==========================
    incidents = []
    current = []

    for line in clean_logs:

        if (
            "error" in line
            or "warn" in line
            or "failed" in line
            or "timeout" in line
            or "denied" in line
            or "crash" in line
        ):

            if current:
                incidents.append(
                    " ".join(current)
                )

            current = [line]

        else:
            current.append(line)

    if current:
        incidents.append(
            " ".join(current)
        )

    results = []

    # ==========================
    # MODEL PREDICTION
    # ==========================
    for incident in incidents:

        vec_cat = (
            tfidf_category
            .transform([incident])
        )

        vec_sev = (
            tfidf_severity
            .transform([incident])
        )

        vec_rc = (
            tfidf_rootcause
            .transform([incident])
        )

        category = (
            category_model
            .predict(vec_cat)[0]
        )

        severity = (
            severity_model
            .predict(vec_sev)[0]
        )

        root_encoded = (
            rootcause_model
            .predict(vec_rc)
        )

        root_cause = (
            rootcause_encoder
            .inverse_transform(
                root_encoded
            )[0]
        )

        fix = fix_mapping.get(
            root_cause,
            "No suggestion"
        )

        results.append({
            "incident": incident,
            "category": category,
            "severity": severity,
            "root_cause": root_cause,
            "suggested_fix": fix
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
