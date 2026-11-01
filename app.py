from contextlib import closing
from pathlib import Path
import sqlite3

import joblib
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

MODEL_PATH = "models/random_forest.joblib"
DATABASE_PATH = Path(__file__).resolve().parent / "maternal_health.db"
app.config["DATABASE"] = str(DATABASE_PATH)
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


def get_db_connection():
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    return connection


@app.before_request
def initialize_database():
    with closing(get_db_connection()) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS patient_records (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT NOT NULL,
                    Age REAL NOT NULL,
                    SystolicBP REAL NOT NULL,
                    DiastolicBP REAL NOT NULL,
                    BS REAL NOT NULL,
                    BodyTemp REAL NOT NULL,
                    HeartRate REAL NOT NULL,
                    risk_level TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
                )
                """
            )


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None
    success_message = None

    if request.method == "POST":
        try:
            patient_name = request.form["patient_name"].strip()
            if not patient_name:
                raise ValueError("Patient name is required.")

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

            with closing(get_db_connection()) as connection:
                with connection:
                    connection.execute(
                        """
                        INSERT INTO patient_records (
                            patient_name, Age, SystolicBP, DiastolicBP,
                            BS, BodyTemp, HeartRate, risk_level
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            patient_name,
                            values["Age"],
                            values["SystolicBP"],
                            values["DiastolicBP"],
                            values["BS"],
                            values["BodyTemp"],
                            values["HeartRate"],
                            str(raw_prediction),
                        ),
                    )

        except (KeyError, ValueError):
            error = "Please enter a valid number in every field and a patient name."

    search_id = request.args.get("patient_id", "").strip()
    deleted_id = request.args.get("deleted", "").strip()
    if deleted_id.isdigit():
        success_message = f"Patient record {deleted_id} was deleted."

    with closing(get_db_connection()) as connection:
        if search_id:
            try:
                patient_id = int(search_id)
            except ValueError:
                error = "Patient ID must be a whole number."
                records = []
            else:
                records = connection.execute(
                    "SELECT * FROM patient_records WHERE patient_id = ?",
                    (patient_id,),
                ).fetchall()
                if not records:
                    error = f"No patient found with ID {patient_id}."
        else:
            records = connection.execute(
                "SELECT * FROM patient_records ORDER BY patient_id DESC"
            ).fetchall()

        statistics = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(CASE WHEN risk_level = 'low risk' THEN 1 ELSE 0 END), 0) AS low,
                COALESCE(SUM(CASE WHEN risk_level = 'mid risk' THEN 1 ELSE 0 END), 0) AS medium,
                COALESCE(SUM(CASE WHEN risk_level = 'high risk' THEN 1 ELSE 0 END), 0) AS high
            FROM patient_records
            """
        ).fetchone()

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        records=records,
        statistics=statistics,
        search_id=search_id,
        success_message=success_message,
    )


@app.route("/patients/<int:patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
    with closing(get_db_connection()) as connection:
        with connection:
            cursor = connection.execute(
                "DELETE FROM patient_records WHERE patient_id = ?",
                (patient_id,),
            )

    if cursor.rowcount:
        return redirect(url_for("home", deleted=patient_id))
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)