import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

DATA_PATH = "data/Maternal Health Risk Data Set.csv"
MODEL_PATH = "models/random_forest.joblib"

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["RiskLevel"])
y = df["RiskLevel"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

print("Confusion matrix:")
print(confusion_matrix(y_test, predictions))

joblib.dump(model, MODEL_PATH)
print(f"\nSaved model to: {MODEL_PATH}")