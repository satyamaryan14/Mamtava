import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1. CREATE SYNTHETIC DATA (The "Textbook" for the AI)
# We are teaching it patterns: High BP + Low Iron = High Risk
data = {
    'Age': [25, 35, 29, 30, 22, 35, 40, 28, 23, 32],
    'SystolicBP': [120, 140, 130, 150, 110, 160, 155, 115, 118, 145],
    'DiastolicBP': [80, 95, 85, 100, 70, 100, 110, 75, 78, 90],
    'Hemoglobin': [12.0, 9.5, 11.0, 8.0, 13.0, 7.5, 8.5, 12.5, 13.5, 9.0],
    'Glucose': [90, 140, 100, 160, 85, 180, 200, 92, 88, 150],
    'RiskLevel': [0, 1, 0, 1, 0, 1, 1, 0, 0, 1] # 0 = Low Risk, 1 = High Risk
}

df = pd.DataFrame(data)

# 2. SEPARATE FEATURES (Inputs) AND TARGET (Output)
X = df[['Age', 'SystolicBP', 'DiastolicBP', 'Hemoglobin', 'Glucose']]
y = df['RiskLevel']

# 3. TRAIN THE MODEL (The Learning Process)
# We use Random Forest because it is accurate for medical data
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. SAVE THE BRAIN (Pickle)
# This saves the trained intelligence into a file we can load later
with open('mamtava_risk_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ AI Model Trained Successfully!")
print("Saved as 'mamtava_risk_model.pkl'")
print("You can now run 'python app.py'")