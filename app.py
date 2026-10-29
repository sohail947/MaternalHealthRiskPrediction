import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

MODEL_PATH = "models/random_forest.joblib"
model = joblib.load(MODEL_PATH)
DISPLAY_LABELS = {
    "low risk": "Low Risk",
    "mid risk": "Mid Risk",
    "high risk": "High Risk",
}

FEATURE_COLUMNS = [
    "Age",
    "SystolicBP",
    "DiastolicBP",
    "BS",
    "BodyTemp",
    "HeartRate",
]


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            values = {
                "Age": float(request.form["Age"]),
                "SystolicBP": float(request.form["SystolicBP"]),
                "DiastolicBP": float(request.form["DiastolicBP"]),
                "BS": float(request.form["BS"]),
                "BodyTemp": float(request.form["BodyTemp"]),
                "HeartRate": float(request.form["HeartRate"]),
            }

            input_data = pd.DataFrame([values], columns=FEATURE_COLUMNS)
           raw_prediction = model.predict(input_data)[0]
           prediction = DISPLAY_LABELS[raw_prediction]

        except (KeyError, ValueError):
            error = "Please enter a valid number in every field."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)