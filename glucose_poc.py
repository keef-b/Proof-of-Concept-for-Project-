import sqlite3
from datetime import datetime, timedelta
import random

# Connect to database
conn = sqlite3.connect("glucose.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    timestamp TEXT,
    glucose_value REAL,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    alert_type TEXT,
    timestamp TEXT,
    message TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);
""")

conn.commit()

# Insert one sample patient
cursor.execute("DELETE FROM patients")
cursor.execute("DELETE FROM readings")
cursor.execute("DELETE FROM alerts")
cursor.execute("INSERT INTO patients (name, dob) VALUES (?, ?)", ("John Doe", "1985-03-14"))
conn.commit()

# Generate sample readings over the past 30 days
now = datetime.now()
for i in range(300):  # 10 readings per day roughly
    days_ago = random.randint(0, 30)
    timestamp = (now - timedelta(days=days_ago, hours=random.randint(0, 23))).isoformat()
    glucose_value = random.uniform(60, 220)
    cursor.execute("INSERT INTO readings (patient_id, timestamp, glucose_value) VALUES (?, ?, ?)", (1, timestamp, glucose_value))

conn.commit()

# Generate alerts for high/low glucose
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

print("✅ Database populated with realistic data over 30 days!")
