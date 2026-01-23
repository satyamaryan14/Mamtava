import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1. Create Synthetic Data (The "Experience" for the AI)
# We teach it patterns: High BP + Low Iron = DANGER
data = {
    'Age': [22, 25, 30, 35, 19, 28, 32, 24, 21, 29],
    'SystolicBP': [110, 120, 145, 160, 115, 130, 150, 118, 90, 135],
    'DiastolicBP': [70, 80, 95, 100, 75, 85, 100, 78, 60, 90],
    'Hemoglobin': [11.5, 12.0, 8.5, 7.0, 10.5, 9.5, 8.0, 11.0, 12.5, 9.0],
    'Glucose': [90, 85, 130, 160, 88, 110, 150, 92, 85, 120],
    # 0 = Low Risk, 1 = High Risk
    'RiskLabel': [0, 0, 1, 1, 0, 0, 1, 0, 0, 1] 
}

df = pd.DataFrame(data)

# 2. Features (X) and Target (y)
X = df[['Age', 'SystolicBP', 'DiastolicBP', 'Hemoglobin', 'Glucose']]
y = df['RiskLabel']

# 3. Train the Model
rf_model = RandomForestClassifier(n_estimators=50, random_state=42)
rf_model.fit(X, y)

# 4. Save the "Brain" to a file
with open('mamtava_risk_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

print("✅ AI Model Trained & Saved as 'mamtava_risk_model.pkl'")