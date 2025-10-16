import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("glucose.db")
cursor = conn.cursor()

# Make sure we have a patient
cursor.execute("SELECT * FROM patients WHERE name=?", ("John Doe",))
patient = cursor.fetchone()
if not patient:
    cursor.execute("INSERT INTO patients (name, dob) VALUES (?, ?)", ("John Doe", "1985-03-14"))
    conn.commit()
    patient_id = cursor.lastrowid
else:
    patient_id = patient[0]

# Generate 500 readings for past 30 days
for i in range(500):
    # Random timestamp in past 30 days
    random_days = random.randint(0, 29)
    random_seconds = random.randint(0, 24*3600)
    timestamp = (datetime.now() - timedelta(days=random_days, seconds=random_seconds)).isoformat()

    # Random glucose value
    glucose_value = random.gauss(120, 40)  # mean 120 mg/dL, sd 40
    glucose_value = max(40, min(250, glucose_value))  # keep in realistic bounds

    cursor.execute("INSERT INTO readings (patient_id, timestamp, glucose_value) VALUES (?, ?, ?)",
                   (patient_id, timestamp, glucose_value))

conn.commit()

# Generate alerts automatically
rows = cursor.execute("SELECT patient_id, glucose_value, timestamp FROM readings").fetchall()
for r in rows:
    if r[1] < 70:
        cursor.execute("INSERT INTO alerts (patient_id, alert_type, timestamp, message) VALUES (?, ?, ?, ?)",
                       (r[0], "LOW", r[2], "⚠️ Low glucose detected!"))
    elif r[1] > 180:
        cursor.execute("INSERT INTO alerts (patient_id, alert_type, timestamp, message) VALUES (?, ?, ?, ?)",
                       (r[0], "HIGH", r[2], "⚠️ High glucose detected!"))

conn.commit()
conn.close()
print("✅ Sample data generated!")
