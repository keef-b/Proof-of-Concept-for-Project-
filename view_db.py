import sqlite3

conn = sqlite3.connect("glucose.db")
cursor = conn.cursor()

print("📋 Patients:")
for row in cursor.execute("SELECT * FROM patients"):
    print(row)

print("\n📊 Readings (latest 10):")
for row in cursor.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 10"):
    print(row)

print("\n🚨 Alerts (latest 10):")
for row in cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 10"):
    print(row)

conn.close()

