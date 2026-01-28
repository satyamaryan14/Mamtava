from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from textblob import TextBlob
import pandas as pd
import numpy as np
import pickle
import os
import random

app = Flask(__name__)
# 1. INIT SOCKET.IO (The Real-Time Bridge)
socketio = SocketIO(app, cors_allowed_origins="*")

# 2. LOAD THE AI MODEL
model_path = 'mamtava_risk_model.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        risk_model = pickle.load(f)
    print("✅ AI Model Loaded")
else:
    risk_model = None
    print("⚠️ Model not found. Run train_model.py first.")

# In-Memory Database for Demo
patient_reports = []

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('patient.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

# --- API: GOVT STORES (For Leaflet Map) ---
@app.route('/api/govt_stores', methods=['GET'])
def get_govt_stores():
    # Simulated Geospatial Data (Open Govt Data format)
    stores = [
        {"name": "PM Jan Aushadhi Kendra (Sec 4)", "stock": "High Stock 🟢"},
        {"name": "Civil Hospital Pharmacy", "stock": "Moderate 🟡"},
        {"name": "Red Cross Medical Store", "stock": "Available 🟢"},
        {"name": "Community Health Center", "stock": "Emergency Only 🔴"}
    ]
    return jsonify(stores)

# --- API: WELLNESS PLAN (For Diet Card) ---
@app.route('/api/get_wellness_plan', methods=['GET'])
def get_wellness_plan():
    return jsonify({
        "meals": [
            {"time": "Morning", "food": "Soaked Almonds + Milk 🥛"},
            {"time": "Lunch", "food": "2 Roti + Spinach (Palak) + Dal 🥗"},
            {"time": "Evening", "food": "Roasted Chana (Iron Rich) 🥜"},
            {"time": "Dinner", "food": "Khichdi + Ghee (Easy Digest) 🍲"}
        ]
    })

# --- API: DOCTOR HISTORY ---
@app.route('/api/doctor/updates', methods=['GET'])
def get_doctor_updates():
    return jsonify(patient_reports)

# --- SOCKET: EMERGENCY SOS LISTENER ---
@socketio.on('trigger_sos')
def handle_sos(data):
    print(f"🚨 SOS RECEIVED from {data.get('lat')}, {data.get('lng')}")
    
    report = {
        "name": "Anjali Sharma",
        "mood": "Panic 😫",
        "vitals": "HR: 120 bpm | GPS Active",
        "symptoms": "🚨 EMERGENCY SOS BUTTON PRESSED",
        "risk": "Critical",
        "risk_score": 100,
        "action": "🚑 DISPATCH AMBULANCE"
    }
    
    patient_reports.append(report)
    emit('doctor_alert', report, broadcast=True)

# --- API: AI VOICE ANALYSIS (The Core Feature) ---
@app.route('/api/analyze_voice', methods=['POST'])
def analyze_voice():
    data = request.json
    text = data.get('text', '')
    
    # A. NLP Analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    mood = "Calm 😌"
    if sentiment < -0.1: mood = "Anxious 😟"
    if sentiment < -0.5: mood = "Distressed 😫"

    # B. Symptom Extraction
    text_lower = text.lower()
    symptoms = []
    if 'headache' in text_lower: symptoms.append('Headache')
    if 'dizzy' in text_lower: symptoms.append('Dizziness')
    if 'pain' in text_lower: symptoms.append('Abd. Pain')
    if 'vomit' in text_lower: symptoms.append('Vomiting')
    if 'bleeding' in text_lower: symptoms.append('Bleeding')

    # C. Vitals Simulation (Hardware Integration Placeholder)
    # If user mentions dizziness, we simulate High BP for the demo
    if 'dizzy' in text_lower or 'headache' in text_lower:
        systolic = random.randint(145, 160)
        diastolic = random.randint(95, 100)
        hb = random.uniform(8.0, 10.5) # Anemic
    else:
        systolic = random.randint(110, 125)
        diastolic = random.randint(70, 85)
        hb = random.uniform(11.0, 13.0)

    # D. AI PREDICTION (Random Forest)
    risk_label = "Low"
    risk_score = 15
    action = "✅ Continue Home Care"

    if risk_model:
        # Prepare Dataframe for Model (Matches training columns)
        # Columns: Age, SystolicBP, DiastolicBP, Hemoglobin, Glucose
        input_data = pd.DataFrame([[25, systolic, diastolic, hb, 120]], 
                                  columns=['Age', 'SystolicBP', 'DiastolicBP', 'Hemoglobin', 'Glucose'])
        
        prediction = risk_model.predict(input_data)[0]
        
        if prediction == 1: # High Risk Class
            risk_label = "Critical"
            risk_score = 92
            action = "⚠️ URGENT HOSPITAL VISIT"
        elif 'bleeding' in text_lower: # Rule-based override
            risk_label = "Critical"
            risk_score = 98
            action = "🚑 IMMEDIATE ER VISIT"
    
    # E. Create Report
    report = {
        "name": "Anjali Sharma",
        "mood": mood,
        "vitals": f"BP: {systolic}/{diastolic} | Hb: {hb:.1f}",
        "symptoms": ", ".join(symptoms) if symptoms else "General Checkup",
        "risk": risk_label,
        "risk_score": risk_score,
        "action": action
    }
    
    # Save & Broadcast if risk is high
    patient_reports.append(report)
    if risk_label in ["High", "Critical"]:
        socketio.emit('doctor_alert', report)

    return jsonify(report)

if __name__ == '__main__':
    # USE SOCKETIO.RUN INSTEAD OF APP.RUN
    socketio.run(app, debug=True, port=5000)