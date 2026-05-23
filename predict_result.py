import re
import joblib
import pandas as pd


# ==========================================
# STEP 1: LOAD TRAINED MODELS
# ==========================================
category_model = joblib.load(
    "category_model.pkl"
)

severity_model = joblib.load(
    "severity_model.pkl"
)

rootcause_model = joblib.load(
    "rootcause_model.pkl"
)

tfidf_category = joblib.load(
    "tfidf.pkl"
)

tfidf_severity = joblib.load(
    "tfidf_severity.pkl"
)

tfidf_rootcause = joblib.load(
    "tfidf_rootcause.pkl"
)

rootcause_encoder = joblib.load(
    "rootcause_encoder.pkl"
)

print("Models Loaded Successfully")


# ==========================================
# STEP 2: LOAD DATASET
# For suggested fix lookup
# ==========================================
df = pd.read_csv("devops_logs_5000.csv")

fix_mapping = (
    df.groupby("root_cause")
    ["suggested_fix"]
    .first()
    .to_dict()
)


# ==========================================
# STEP 3: READ LOG FILE
# ==========================================
log_file_path = "server.log"

with open(log_file_path, "r",
          encoding="utf-8") as file:
    logs = file.readlines()

print("Log file loaded")


# ==========================================
# STEP 4: PARSER ENGINE
# Remove timestamps/noise
# ==========================================
clean_logs = []

for line in logs:

    line = line.strip()

    # Skip INFO & DEBUG
    if ("INFO" in line or
            "DEBUG" in line):
        continue

    # Remove timestamp
    line = re.sub(
        r'\d{4}-\d{2}-\d{2}.*?',
        '',
        line
    )

    line = re.sub(
        r'[^a-zA-Z0-9 ]',
        ' ',
        line
    )

    line = line.lower()

    if len(line) > 5:
        clean_logs.append(line)

print("Log cleaning completed")


# ==========================================
# STEP 5: INCIDENT GROUPING
# Group by ERROR/WARN blocks
# ==========================================
incidents = []

current_incident = []

for line in clean_logs:

    if (
        "error" in line
        or "warn" in line
        or "failed" in line
        or "exception" in line
        or "timeout" in line
        or "denied" in line
        or "crash" in line
    ):

        if current_incident:
            incidents.append(
                " ".join(
                    current_incident
                )
            )

        current_incident = [line]

    else:
        current_incident.append(line)


if current_incident:
    incidents.append(
        " ".join(current_incident)
    )

print(
    f"Detected {len(incidents)} incidents"
)


# ==========================================
# STEP 6: PREDICT INCIDENTS
# ==========================================
print("\n========== RESULTS ==========\n")

for i, incident in enumerate(
        incidents, start=1):

    # Vectorize
    vec_category = (
        tfidf_category
        .transform([incident])
    )

    vec_severity = (
        tfidf_severity
        .transform([incident])
    )

    vec_rootcause = (
        tfidf_rootcause
        .transform([incident])
    )

    # Predictions
    category = (
        category_model
        .predict(vec_category)[0]
    )

    severity = (
        severity_model
        .predict(vec_severity)[0]
    )

    rootcause_encoded = (
        rootcause_model
        .predict(vec_rootcause)
    )

    rootcause = (
        rootcause_encoder
        .inverse_transform(
            rootcause_encoded
        )[0]
    )

    # Suggested fix
    suggested_fix = (
        fix_mapping.get(
            rootcause,
            "No suggestion available"
        )
    )

    # Print output
    print(
        f"========== INCIDENT {i} =========="
    )

    print(
        f"Category      : {category}"
    )

    print(
        f"Severity      : {severity}"
    )

    print(
        f"Root Cause    : {rootcause}"
    )

    print(
        f"Suggested Fix : "
        f"{suggested_fix}"
    )

    print(
        "=" * 35
    )
