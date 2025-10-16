import csv
from datetime import datetime, timedelta
import random

# CSV filename
filename = "sample_glucose.csv"

# Open file for writing
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["timestamp", "glucose_value"])
    
    # Generate 300 readings over the past 30 days (~10 per day)
    now = datetime.now()
    for i in range(300):
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        timestamp = (now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)).isoformat()
        glucose_value = round(random.uniform(60, 220), 1)
        writer.writerow([timestamp, glucose_value])

print(f"✅ CSV file '{filename}' created with 300 sample readings!")
