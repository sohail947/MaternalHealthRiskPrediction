
# Maternal Health Risk Level Prediction

Educational machine-learning prototype that predicts low risk, mid risk, or high risk.

This is not a medical diagnosis tool.

## Dataset

Source: UCI Machine Learning Repository - Maternal Health Risk dataset.

Local file: data/Maternal Health Risk Data Set.csv

The inspected local file contains:
- 1,014 rows
- 7 columns
- 6 input features
- Target column: RiskLevel
- No missing values

Input features:
- Age
- SystolicBP
- DiastolicBP
- BS
- BodyTemp
- HeartRate

## Models evaluated

All models used the same stratified 80/20 split with random_state=42.

Logistic Regression: Accuracy 0.6010, Macro F1 0.5953
Decision Tree: Accuracy 0.8424, Macro F1 0.8493
Random Forest: Accuracy 0.8621, Macro F1 0.8698

Random Forest was selected because it performed best in this comparison.

## Run the application

1. Activate the environment:
   .venv\Scripts\activate

2. Start Flask:
   python app.py

3. Open this address:
   http://127.0.0.1:5000

## Patient records and dashboard

The app creates `maternal_health.db` in the project folder automatically.
After a successful prediction, it saves the patient's name, an automatically
assigned Patient ID, the six measurements, the predicted risk, and the date
and time of the prediction. The page shows all saved records and total, low,
medium, and high risk counts. Use the Patient ID search field to find a
record, or its Delete button to remove it.

The database contains health information and patient names. Keep it private,
use only information you are permitted to store, and do not treat this
educational application as a medical records system.

Run the app tests with:

   python -m unittest discover -s tests

## Important files

app.py - Flask application
src/prepare_data.py - data loading and splitting
src/train_model.py - Random Forest training
src/compare_models.py - model comparison
src/predict_one.py - one-row prediction test
models/random_forest.joblib - saved model
templates/index.html - web form
maternal_health.db - SQLite patient records (created automatically)
requirements.txt - package versions
