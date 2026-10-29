import joblib
import pandas as pd

DATA_PATH = "data/Maternal Health Risk Data Set.csv"
MODEL_PATH = "models/random_forest.joblib"

feature_columns = [
    "Age",
    "SystolicBP",
    "DiastolicBP",
    "BS",
    "BodyTemp",
    "HeartRate",
]

df = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)

sample = df[feature_columns].iloc[[0]]
prediction = model.predict(sample)[0]
actual_risk = df["RiskLevel"].iloc[0]

print("Input values:")
print(sample.to_dict("records")[0])
print("Predicted risk:", prediction)
print("Actual risk:", actual_risk)