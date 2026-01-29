# MongoDB Integration – Mamatva

## MongoDB Atlas Setup
- Free M0 cluster created
- Cloud provider: AWS
- Database name: mamatva_db

## Connection String (Masked)
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority

> Note: Actual credentials are stored securely and not exposed publicly.

## Planned Collections

### patients
```json
{
  "patient_id": "P001",
  "name": "Anita Sharma",
  "age": 28,
  "pregnancy_week": 24,
  "created_at": "timestamp"
}
{
  "patient_id": "P001",
  "bp": 140,
  "bmi": 32.4,
  "risk_level": "High",
  "predicted_at": "timestamp"
}
{
  "doctor_id": "D001",
  "name": "Dr. Mehta",
  "hospital": "City Hospital",
  "email": "drmehta@gmail.com"
}
{
  "patient_id": "P002",
  "name": "Ria Yadav",
  "age": 34,
  "pregnancy_week": 12,
  "created_at": "timestamp"
}
{
  "patient_id": "P002",
  "bp": 130,
  "bmi": 30.2,
  "risk_level": "Low",
  "predicted_at": "timestamp"
}
{
  "doctor_id": "D002",
  "name": "Dr. Singh",
  "hospital": "Medanta Hospital",
  "email": "drsingh101@gmail.com"
}
{
  "patient_id": "P003",
  "name": "Pehal Sharma",
  "age": 23,
  "pregnancy_week": 2,
  "created_at": "timestamp"
}
{
  "patient_id": "P003",
  "bp": 150,
  "bmi": 30.6,
  "risk_level": "High",
  "predicted_at": "timestamp"
}
{
  "doctor_id": "D003",
  "name": "Dr. Rajawat",
  "hospital": "Rajawat Hospital",
  "email": "drraja899@gmail.com"
}
{
  "patient_id": "P004",
  "name": "manya chugh",
  "age": 30,
  "pregnancy_week": 8,
  "created_at": "timestamp"
}
{
  "patient_id": "P004",
  "bp": 140,
  "bmi": 29.8,
  "risk_level": "High",
  "predicted_at": "timestamp"
}
{
  "doctor_id": "D004",
  "name": "Dr. Patel",
  "hospital": "Artemis Hospital",
  "email": "drpatel@gmail.com"
}
