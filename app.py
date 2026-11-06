import os
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

# Settings come from environment variables, with safe defaults for local use
allowed = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:5500"
)
CORS(app, origins=[o.strip() for o in allowed.split(",") if o.strip()])

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

# In-memory storage: lost when the server stops or restarts
egg_records = []


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/eggs", methods=["POST"])
def add_egg_record():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    shed = str(data.get("shed", "")).strip()
    date = data.get("date")
    count = data.get("count")

    if not shed or not date or count is None:
        return jsonify({"error": "shed, date and count are all required"}), 400

    if not isinstance(count, int) or count < 0:
        return jsonify({"error": "count must be a whole number, 0 or more"}), 400

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return jsonify({"error": "date must look like 2026-11-02"}), 400

    record = {"shed": shed, "date": date, "count": count}
    egg_records.append(record)

    return jsonify({"message": "Record saved", "record": record}), 201


@app.route("/api/eggs", methods=["GET"])
def get_egg_records():
    total = sum(record["count"] for record in egg_records)

    return jsonify({
        "records": egg_records,
        "record_count": len(egg_records),
        "total_eggs": total
    }), 200


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")