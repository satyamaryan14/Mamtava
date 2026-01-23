from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import random
import pickle
import numpy as np
import os

app = Flask(__name__)

# --- 1. LOAD THE AI MODEL ---
model_path = 'mamtava_risk_model.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        risk_model = pickle.load(f)
    print("✅ AI Model Loaded Successfully")
else:
    risk_model = None
    print("⚠️ Warning: Model not found. Run train_model.py first.")

# --- IN-MEMORY DATABASE ---
patient_reports = []

@app.route('/')
def home():
    return render_template('patient.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

# --- GOVT DATA API ---
@app.route('/api/govt_stores', methods=['GET'])
def get_govt_stores():
    stores = [
        {"name": "Jan Aushadhi Kendra #102", "distance": "0.8 km", "type": "Pharmacy", "stock": "High"},
        {"name": "Civil Hospital Blood Bank", "distance": "2.1 km", "type": "Emergency", "stock": "Moderate"},
        {"name": "Community Health Center", "distance": "3.5 km", "type": "Clinic", "stock": "Available"}
    ]
    return jsonify(stores)

# --- WELLNESS API ---
@app.route('/api/get_wellness_plan', methods=['GET'])
def get_wellness_plan():
    plan = {
        "calories": "2,400 kcal",
        "meals": [
            {"time": "Breakfast", "food": "2 Moong Dal Chilas + Milk", "cal": "400"},
            {"time": "Lunch", "food": "2 Roti + Palak Paneer", "cal": "650"},
            {"time": "Dinner", "food": "Khichdi with Ghee", "cal": "450"}
        ],
        "exercises": [
            {"name": "Butterfly Pose", "duration": "10 mins"},
            {"name": "Walking", "duration": "20 mins"}
        ]
    }
    return jsonify(plan)

# --- DOCTOR UPDATES API ---
@app.route('/api/doctor/updates', methods=['GET'])
def get_doctor_updates():
    return jsonify(patient_reports)

# --- 3. THE CORE AI ENGINE ---
@app.route('/api/analyze_voice', methods=['POST'])
def analyze_voice():
    data = request.json
    text = data.get('text', '')
    
    # A. NLP SENTIMENT ANALYSIS
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity 
    mood = "Calm 😌"
    if sentiment_score < -0.1: mood = "Anxious 😟"
    if sentiment_score < -0.4: mood = "Panic 😫"

    # B. EXTRACT SYMPTOMS
    text_lower = text.lower()
    symptoms = []
    if 'headache' in text_lower: symptoms.append('Headache')
    if 'dizzy' in text_lower: symptoms.append('Dizziness')
    if 'pain' in text_lower: symptoms.append('Abd. Pain')
    if 'swelling' in text_lower: symptoms.append('Edema')
    
    # C. HARDWARE SIMULATION (Generates Vitals)
    # In real life, these come from sensors. For Hackathon, we simulate High BP if "dizzy".
    if 'dizzy' in text_lower or 'pain' in text_lower:
        systolic = random.randint(140, 160) # Simulate High BP
        hemoglobin = random.uniform(8.0, 10.0) # Simulate Anemia
    else:
        systolic = random.randint(110, 130) # Normal BP
        hemoglobin = random.uniform(11.0, 13.0) # Normal Iron

    diastolic = systolic - 40
    glucose = random.randint(80, 140)
    age = 25 # Assume avg age for demo

    # D. PREDICT RISK USING RANDOM FOREST (The Real AI)
    risk_label = "Low"
    risk_score = 10 # Default
    
    if risk_model:
        # Input: [Age, Systolic, Diastolic, Hemoglobin, Glucose]
        patient_data = np.array([[age, systolic, diastolic, hemoglobin, glucose]])
        prediction = risk_model.predict(patient_data) # 0 or 1
        
        if prediction[0] == 1:
            risk_label = "Critical"
            risk_score = 95
            action = "🚑 DISPATCH AMBULANCE"
        else:
            risk_label = "Low"
            risk_score = 25
            action = "✅ Home Rest"
            
        # Override if Mood is Panic
        if mood == "Panic 😫" and risk_label == "Low":
            risk_label = "High"
            risk_score = 65
            action = "⚠️ Counselor Consult"
    else:
        action = "⚠️ AI Offline"

    # Save to "Database"
    new_report = {
        "name": "Anjali Sharma",
        "symptoms": ", ".join(symptoms) if symptoms else "None",
        "vitals": f"BP: {systolic}/{diastolic} | Hb: {hemoglobin:.1f}",
        "risk": risk_label,
        "risk_score": risk_score,
        "mood": mood,
        "action": action
    }
    patient_reports.append(new_report)

    return jsonify({
        "detected_symptoms": symptoms,
        "mood": mood,
        "risk": risk_label,
        "action": action
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)