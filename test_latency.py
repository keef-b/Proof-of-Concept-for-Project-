import requests
import time
import csv
from io import BytesIO

# Your running Flask app
BASE_URL = "http://127.0.0.1:5000"

# ------------- CONFIG -------------
CSV_FILE = "sample_glucose.csv"  # A CSV you want to upload
LATENCY_THRESHOLD = 2.0  # seconds (adjust if you want)
# ---------------------------------

def measure_upload_latency():
    with open(CSV_FILE, "rb") as f:
        files = {"file": (CSV_FILE, f, "text/csv")}
        start = time.time()
        response = requests.post(f"{BASE_URL}/upload", files=files)
        end = time.time()
    duration = end - start
    return duration, response.status_code

def measure_retrieval_latency():
    start = time.time()
    response = requests.get(f"{BASE_URL}/readings_json")
    end = time.time()
    duration = end - start
    return duration, response.status_code, len(response.json())

def main():
    print("🚀 Running System Latency Test...\n")

    upload_time, upload_status = measure_upload_latency()
    print(f"📤 Upload Time: {upload_time:.3f}s (Status: {upload_status})")

    retrieval_time, retrieval_status, record_count = measure_retrieval_latency()
    print(f"📥 Retrieval Time: {retrieval_time:.3f}s (Status: {retrieval_status}, Records: {record_count})")

    total_time = upload_time + retrieval_time
    print(f"\n⏱️ Total System Latency: {total_time:.3f}s")

    if total_time <= LATENCY_THRESHOLD:
        print(f"✅ PASS: System is responsive (under {LATENCY_THRESHOLD}s total)")
    else:
        print(f"❌ FAIL: System latency too high ({total_time:.3f}s)")

if __name__ == "__main__":
    main()
