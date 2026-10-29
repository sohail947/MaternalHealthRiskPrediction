import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

DATA_PATH = "data/Maternal Health Risk Data Set.csv"

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

models = {
    "Logistic Regression": Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    ),
    "Decision Tree": DecisionTreeClassifier(
        random_state=42,
        class_weight="balanced",
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    ),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(y_test, predictions, average="macro")

    print(f"{name}:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  Macro F1: {macro_f1:.4f}")