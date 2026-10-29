import pandas as pd
from sklearn.model_selection import train_test_split

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

print("Total rows:", len(df))
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("Feature columns:", list(X.columns))
print("Training class counts:")
print(y_train.value_counts())
print("Testing class counts:")
print(y_test.value_counts())