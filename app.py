from flask import Flask, jsonify, render_template, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("glucose.db")
    conn.row_factory = sqlite3.Row
    return conn

# API route to get readings (optionally filtered by days)
@app.route("/readings_json")
def readings_json():
    days = request.args.get("days", default=None, type=int)
    conn = get_db_connection()
    if days:
        since = (datetime.now() - timedelta(days=days)).isoformat()
        rows = conn.execute("SELECT * FROM readings WHERE timestamp >= ?", (since,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM readings").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# Dashboard route
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, jsonify, render_template, request
import sqlite3
import csv
from io import TextIOWrapper
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("glucose.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Existing routes here: /readings_json, /dashboard etc. ---

# --- New route: Upload CSV ---
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "No file uploaded", 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Parse CSV
        csv_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        for row in reader:
            timestamp = row.get("timestamp") or datetime.now().isoformat()
            glucose_value = float(row["glucose_value"])
            cursor.execute("INSERT INTO readings (patient_id, timestamp, glucose_value) VALUES (?, ?, ?)",
                           (1, timestamp, glucose_value))
        conn.commit()
        conn.close()
        return "✅ File uploaded and readings added!"
    
    # GET request shows a simple upload form
    return '''
    <h3>Upload Glucose CSV</h3>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required>
        <input type="submit" value="Upload">
    </form>
    '''
