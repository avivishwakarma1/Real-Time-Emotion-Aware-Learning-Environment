import os
import base64
import csv
from datetime import datetime
import numpy as np
import pandas as pd
import cv2
from flask import Flask, request, jsonify, render_template, send_file
from deepface import DeepFace
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enables cross-origin requests

cascade_path = "haarcascade_frontalface_default.xml"
if os.path.exists(cascade_path):
    face_cascade = cv2.CascadeClassifier(cascade_path)
else:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# --- Logging Setup ---
os.makedirs("logs", exist_ok=True)
LOG_FILE = "logs/emotions.csv"

def ensure_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "user_id", "role", "emotion", "confidence", "engagement"])

def map_emotion_to_engagement(emotion):
    m = {
        "happy": 0.92, "excited": 0.95, "surprise": 0.82,
        "neutral": 0.6, "sad": 0.32, "angry": 0.18,
        "fear": 0.25, "disgust": 0.15, "unknown": 0.0
    }
    return m.get(emotion.lower(), 0.0)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    image_data_url = data.get("image", "")
    user_id = data.get("user_id", "anonymous").strip()
    role = data.get("role", "student")

    if "base64," in image_data_url:
        base64_img = image_data_url.split(",")[1]
    else:
        return jsonify({"status": "error", "message": "Invalid image format"}), 400

    try:
        image_bytes = base64.b64decode(base64_img)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Decoding Error: {e}")
        return jsonify({"status": "error", "message": "Image decoding failed"}), 400

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    if len(faces) == 0:
        return jsonify({"status": "warning", "emotion": "No Face", "confidence": 0.0, "engagement": 0.0})

    (x, y, w, h) = faces[0]
    face_img = frame[y:y+h, x:x+w]

    try:
        result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
    except Exception as e:
        print(f"DeepFace Error: {e}")
        return jsonify({"status": "error", "message": "Analysis failed"}), 500

    res = result[0] if isinstance(result, list) else result
    dominant = res.get("dominant_emotion", "unknown")
    confidence = float(res.get("emotion", {}).get(dominant, 0.0))
    engagement = map_emotion_to_engagement(dominant)
    timestamp = datetime.utcnow().isoformat()

    ensure_log()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, user_id, role, dominant, confidence, engagement])

    return jsonify({"status": "ok", "emotion": dominant, "confidence": confidence, "engagement": engagement})

@app.route("/data")
def data():
    if not os.path.exists(LOG_FILE):
        return jsonify({"emotion_counts": {}, "avg_engagement_by_user": [], "recent": []})
    
    df = pd.read_csv(LOG_FILE)
    last = df.tail(500)
    
    emotion_counts = last["emotion"].value_counts().to_dict()
    avg_engagement_by_user = last.groupby("user_id")["engagement"].mean().reset_index().to_dict(orient="records")
    
    return jsonify({"emotion_counts": emotion_counts, "avg_engagement_by_user": avg_engagement_by_user})

@app.route("/download_logs")
def download_logs():
    if not os.path.exists(LOG_FILE):
        return "Log file not found.", 404
    return send_file(LOG_FILE, as_attachment=True, download_name="emotion_logs.csv", mimetype="text/csv")

if __name__ == "__main__":
    # Ensure you create a virtual environment and install the requirements first!
    app.run(debug=True, host='0.0.0.0', port=5000)