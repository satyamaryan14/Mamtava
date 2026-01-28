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
