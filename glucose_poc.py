import sqlite3
from datetime import datetime

# 1️⃣ Connect to the database (creates if not exists)
conn = sqlite3.connect("glucose.db")
cursor = conn.cursor()

# 2️⃣ Create tables (if they don't exist already)
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
print("✅ Database and tables created successfully!")

# 3️⃣ Insert sample patient (only once)
cursor.execute("INSERT INTO patients (name, dob) VALUES (?, ?)", ("John Doe", "1985-03-14"))
conn.commit()

# 4️⃣ Insert sample glucose readings
glucose_values = [85, 120, 190, 68, 140, 200, 65]  # mg/dL
for value in glucose_values:
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO readings (patient_id, timestamp, glucose_value) VALUES (?, ?, ?)", (1, timestamp, value))

conn.commit()
print("✅ Sample patient and readings added!")

# 5️⃣ Generate alerts for high/low glucose
rows = cursor.execute("SELECT patient_id, glucose_value, timestamp FROM readings").fetchall()
for r in rows:
    if r[1] < 70:
        cursor.execute("INSERT INTO alerts (patient_id, alert_type, timestamp, message) VALUES (?, ?, ?, ?)",
                       (r[0], "LOW", r[2], "⚠️ Low glucose detected!"))
    elif r[1] > 180:
        cursor.execute("INSERT INTO alerts (patient_id, alert_type, timestamp, message) VALUES (?, ?, ?, ?)",
                       (r[0], "HIGH", r[2], "⚠️ High glucose detected!"))

conn.commit()
print("✅ Alerts generated!")

# 6️⃣ Print database contents to verify
print("\n📋 Readings:")
for r in cursor.execute("SELECT * FROM readings").fetchall():
    print(r)

print("\n🚨 Alerts:")
for a in cursor.execute("SELECT * FROM alerts").fetchall():
    print(a)

# 7️⃣ Close the connection
conn.close()
