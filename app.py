from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
import csv
from io import TextIOWrapper
from datetime import datetime, timedelta

app = Flask(__name__)

# ------------------------------
# Database connection helper
# ------------------------------
def get_db_connection():
    conn = sqlite3.connect("glucose.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------------
# API: Return glucose readings (optionally filtered by days)
# ------------------------------
@app.route("/readings_json")
def readings_json():
    days = request.args.get("days", default=None, type=int)
    conn = get_db_connection()

    if days:
        since = (datetime.now() - timedelta(days=days)).isoformat()
        rows = conn.execute(
            "SELECT * FROM readings WHERE timestamp >= ? ORDER BY timestamp ASC",
            (since,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM readings ORDER BY timestamp ASC").fetchall()

    conn.close()
    return jsonify([dict(r) for r in rows])

# ------------------------------
# Route: Dashboard (main UI)
# ------------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# ------------------------------
# Route: Upload CSV (to add new readings)
# ------------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "❌ No file uploaded", 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Parse uploaded CSV
        csv_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(csv_file)

        for row in reader:
            timestamp = row.get("timestamp") or datetime.now().isoformat()
            glucose_value = float(row["glucose_value"])
            cursor.execute(
                "INSERT INTO readings (patient_id, timestamp, glucose_value) VALUES (?, ?, ?)",
                (1, timestamp, glucose_value)
            )

        conn.commit()
        conn.close()

        # ✅ Redirect back to dashboard after upload
        return redirect(url_for("dashboard"))

    # If GET request, show the upload form
    return '''
    <h3>📤 Upload Glucose CSV</h3>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required>
        <input type="submit" value="Upload">
    </form>
    <p>Example CSV columns: timestamp, glucose_value</p>
    '''

# ------------------------------
# Run the Flask app
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
