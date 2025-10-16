import requests

# -----------------------------
# Config
# -----------------------------
api_url = "http://127.0.0.1:5000/readings_json"  # Flask API URL
tolerance = 0.5  # mg/dL

# -----------------------------
# Expected values (what you know should be in DB)
# -----------------------------
# For example, after upload, these are the first 10 readings in the CSV you uploaded via UI
expected_values = [
    80.1, 131.7, 192.0, 111.7, 101.8,
    121.2, 107.6, 134.2, 112.7, 145.4
]

# -----------------------------
# Get API data (from DB after CSV upload)
# -----------------------------
response = requests.get(api_url)
api_data = response.json()

if not api_data:
    print("❌ No data found in the database via API!")
    exit()

api_values = [float(r["glucose_value"]) for r in api_data[:len(expected_values)]]

# -----------------------------
# Compare values
# -----------------------------
missing_or_wrong = []

for expected_val in expected_values:
    if not any(abs(expected_val - api_val) <= tolerance for api_val in api_values):
        missing_or_wrong.append(expected_val)

# -----------------------------
# Print results
# -----------------------------
if not missing_or_wrong:
    print(f"✅ All expected readings are present in the dashboard API output!")
else:
    print("❌ Some expected readings are missing or outside tolerance:")
    print(missing_or_wrong)
