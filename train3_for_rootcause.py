import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBClassifier


# ------------------------------------------------
# STEP 1: Load Dataset
# ------------------------------------------------
df = pd.read_csv("devops_logs_5000.csv")

print("Dataset Loaded Successfully")
print(df.head())


# ------------------------------------------------
# STEP 2: Clean Dataset
# ------------------------------------------------
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

print("\nDataset Shape:", df.shape)


# ------------------------------------------------
# STEP 3: Features & Labels
# ------------------------------------------------
X = df["log_message"]

y = df["root_cause"]


# ------------------------------------------------
# STEP 4: Encode Root Cause Labels
# ------------------------------------------------
label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\nRoot Cause Labels Encoded")


# ------------------------------------------------
# STEP 5: TF-IDF Vectorization
# ------------------------------------------------
tfidf = TfidfVectorizer(
    lowercase=True,
    stop_words=None,
    ngram_range=(1, 2),
    max_features=10000
)

X_vectorized = tfidf.fit_transform(X)

print("\nTF-IDF Vectorization Completed")


# ------------------------------------------------
# STEP 6: Train-Test Split
# ------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y_encoded,
    test_size=0.2,
    random_state=42
)

print("\nTrain Size:", X_train.shape)
print("Test Size:", X_test.shape)


# ------------------------------------------------
# STEP 7: Train XGBoost Model
# ------------------------------------------------
rootcause_model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    objective="multi:softmax",
    eval_metric="mlogloss",
    random_state=42
)

rootcause_model.fit(X_train, y_train)

print("\nRoot Cause Model Training Completed")


# ------------------------------------------------
# STEP 8: Prediction
# ------------------------------------------------
predictions = rootcause_model.predict(X_test)


# ------------------------------------------------
# STEP 9: Accuracy
# ------------------------------------------------
accuracy = accuracy_score(y_test, predictions)

print("\nRoot Cause Accuracy:",
      round(accuracy * 100, 2), "%")


# ------------------------------------------------
# STEP 10: Classification Report
# ------------------------------------------------
print("\nClassification Report:\n")

decoded_y_test = label_encoder.inverse_transform(y_test)
decoded_predictions = label_encoder.inverse_transform(predictions)

print(classification_report(
    decoded_y_test,
    decoded_predictions
))


# ------------------------------------------------
# STEP 11: Save Model
# ------------------------------------------------
joblib.dump(rootcause_model,
            "rootcause_model.pkl")

joblib.dump(tfidf,
            "tfidf_rootcause.pkl")

joblib.dump(label_encoder,
            "rootcause_encoder.pkl")

print("\nRoot Cause Model Saved Successfully")


# ------------------------------------------------
# STEP 12: Test with Sample Log
# ------------------------------------------------
sample_log = [
    "Pod CrashLoopBackOff OOMKilled"
]

sample_vector = tfidf.transform(sample_log)

prediction_encoded = rootcause_model.predict(
    sample_vector
)

prediction = label_encoder.inverse_transform(
    prediction_encoded
)

print("\nSample Prediction:",
      prediction[0])
