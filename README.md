# Glucose Monitoring Dashboard - Proof of Concept

This repository contains a **proof-of-concept Flask application** for a glucose monitoring dashboard. It demonstrates a full workflow:

- Storing patient glucose readings in a SQLite database.
- Viewing readings on an interactive dashboard with line charts.
- Uploading new glucose readings via CSV through the web interface.
- Basic automated testing to verify uploaded readings are correctly stored and displayed.

---

## 🧩 Features

- **SQLite Database**: Stores patients, glucose readings, and alerts.
- **Flask API**: `/readings_json` returns readings as JSON (optionally filtered by number of days).
- **Interactive Dashboard**: Visualizes glucose readings over time with Chart.js.
  - Filter readings: past week, 2 weeks, month, or all data.
  - Upload CSV files directly from the UI.
- **Alerts**: High and low glucose readings are flagged (optional for future development).
- **Automated Test**: `test_dashboard.py` checks if readings uploaded via the UI are correctly stored in the database and returned by the API.

---

## 📂 File Structure

