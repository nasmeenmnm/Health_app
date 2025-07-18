from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import sqlite3, joblib, pandas as pd, requests
import numpy as np
from tensorflow.keras.models import load_model

main = Blueprint('main', __name__)

@main.route("/dashboard")
@login_required
def dashboard():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, temperature, heart_rate, spo2, ecg, label, Disease, Cause, Symptoms, Solution, Treatment
        FROM health_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (current_user.id,))
    
    rows = cur.fetchall()
    conn.close()

    history = [{
        "timestamp": row[0],
        "temp": row[1],
        "hr": row[2],
        "spo2": row[3],
        "ecg": row[4],
        "label": row[5],
        "Disease":row[6], 
        "Cause":row[7], 
        "Symptoms":row[8], 
        "Solution":row[9], 
        "Treatment":row[10]
    } for row in rows]

    latest_entry = history[0] if history else {}

    label = latest_entry.get("label")
    disease = latest_entry.get("Disease")
    cause = latest_entry.get("Cause")
    symptoms = latest_entry.get("Symptoms")
    solution = latest_entry.get("Solution")
    treatment = latest_entry.get("Treatment")

    return render_template(
        "dashboard.html",
        history=history,
        label=label,
        disease=disease,
        cause=cause,
        symptoms=symptoms,
        solution=solution,
        treatment=treatment
    )

@main.route('/predict', methods=['POST'])
@login_required
def predict():
    username = "safee123"
    aio_key = "aio_fRqa43hqQooVHpsU2VDFpBy7v67P"

    def fetch(feed):
        url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed}/data/last"
        res = requests.get(url, headers={"X-AIO-Key": aio_key})
        return float(res.json()["value"])

    def fetch_series(feed, limit=100):
        url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed}/data?limit={limit}"
        res = requests.get(url, headers={"X-AIO-Key": aio_key})
        return [float(item["value"]) for item in res.json()]

    # --- Fetch sensor values ---
    temp_c = fetch("temperature")
    temp = (temp_c * 9/5) + 32
    hr = fetch("heartrate")
    spo2 = fetch("spo2")
    ecg_series = fetch_series("ecg", limit=100)

    # --- Preprocess ECG for LSTM model ---
    ecg_array = np.array(ecg_series).reshape(1, 100, 1)  # shape: (1, 50, 1)
    ecg_array = ecg_array / 4096.0  # Normalize if needed (depends on training)

    # --- Load LSTM model ---
    lstm_model = load_model("app/model/lstm_model.h5")
    le_ecg = joblib.load("app/model/le_ecg.pkl")

    # --- Predict ECG type ---
    ecg_pred = lstm_model.predict(ecg_array)
    ecg_class_index = np.argmax(ecg_pred)
    ecg_text = le_ecg.inverse_transform([ecg_class_index])[0]
    
    ecg_val = le_ecg.transform([ecg_text])[0]
    X = pd.DataFrame([[temp, hr, spo2, ecg_val]], columns=["Temperature_F", "HeartRate", "SpO2", "ECG_Type_Encoded"])

    # --- Load health model ---
    # --- Load MultiOutput model and encoders ---
    model = joblib.load("app/model/multioutput_model.pkl")
    le_label = joblib.load("app/model/le_label.pkl")
    le_disease = joblib.load("app/model/le_disease.pkl")
    le_cause = joblib.load("app/model/le_cause.pkl")
    le_symptoms = joblib.load("app/model/le_symptoms.pkl")
    le_solution = joblib.load("app/model/le_solution.pkl")
    le_treatment = joblib.load("app/model/le_treatment.pkl")

    # --- Predict multiple outputs ---
    predictions = model.predict(X)[0]
    label = le_label.inverse_transform([predictions[0]])[0]
    disease = le_disease.inverse_transform([predictions[1]])[0]
    cause = le_cause.inverse_transform([predictions[2]])[0]
    symptoms = le_symptoms.inverse_transform([predictions[3]])[0]
    solution = le_solution.inverse_transform([predictions[4]])[0]
    treatment = le_treatment.inverse_transform([predictions[5]])[0]

    
    

    # --- Save to DB ---
    conn = sqlite3.connect("users.db")
    conn.execute('''
        INSERT INTO health_logs (user_id, temperature, heart_rate , spo2, ecg, label, Disease, Cause, Symptoms, Solution, Treatment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (current_user.id, temp, hr, spo2, ecg_text, label, disease, cause, symptoms, solution, treatment))
    conn.commit()
    conn.close()

    return redirect(url_for('main.dashboard'))
