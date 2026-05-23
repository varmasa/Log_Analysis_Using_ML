import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report


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

y = df["category"]


# ------------------------------------------------
# STEP 4: TF-IDF Vectorization
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
# STEP 5: Train-Test Split
# ------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTrain Size:", X_train.shape)
print("Test Size:", X_test.shape)


# ------------------------------------------------
# STEP 6: Train Model (Linear SVM)
# ------------------------------------------------
category_model = LinearSVC()

category_model.fit(X_train, y_train)

print("\nModel Training Completed")


# ------------------------------------------------
# STEP 7: Prediction
# ------------------------------------------------
predictions = category_model.predict(X_test)


# ------------------------------------------------
# STEP 8: Accuracy
# ------------------------------------------------
accuracy = accuracy_score(y_test, predictions)

print("\nCategory Model Accuracy:",
      round(accuracy * 100, 2), "%")


# ------------------------------------------------
# STEP 9: Classification Report
# ------------------------------------------------
print("\nClassification Report:\n")

print(classification_report(
    y_test,
    predictions
))


# ------------------------------------------------
# STEP 10: Save Model
# ------------------------------------------------
joblib.dump(category_model,
            "category_model.pkl")

joblib.dump(tfidf,
            "tfidf.pkl")

print("\nModel Saved Successfully")


# ------------------------------------------------
# STEP 11: Test with Sample Log
# ------------------------------------------------
sample_log = [
    "No space in server"
]

sample_vector = tfidf.transform(sample_log)

prediction = category_model.predict(sample_vector)

print("\nSample Prediction:",
      prediction[0])
