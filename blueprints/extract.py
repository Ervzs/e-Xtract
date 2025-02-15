from flask import Blueprint, render_template, request, jsonify, session, Flask, Response, send_file
import os
import google.generativeai as genai
import cv2
import numpy as np
from ultralytics import YOLO


extract_bp = Blueprint('extract', __name__, static_folder='static', template_folder='templates') #initialize blueprint

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = YOLO(r"models/image-proc/best.pt")  # Load YOLO model

'''
Use only for local servers
cap = cv2.VideoCapture(0)  # Open webcam
'''



@extract_bp.route("/extract")
def extract():
    return render_template("extract.html")

def process_frame(frame):
    results = model(frame, conf=0.6)  # Run YOLO on the frame

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            conf = box.conf[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()

@extract_bp.route("/video_feed", methods=["POST"])
def video_feed():
    file = request.files["frame"].read()
    npimg = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = model(frame, conf=0.6)  # Run YOLO on the frame

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            conf = box.conf[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, buffer = cv2.imencode(".jpg", frame)
    return Response(buffer.tobytes(), mimetype="image/jpeg")


@extract_bp.route("/process_image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify({"error": "No file found"}), 400

    file = request.files["file"].read()
    npimg = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Resized the frame to the model's expected input size to help detect objects better
    frame = cv2.resize(frame, (640, 640))

    results = model(frame, conf=0.1)  # Only works with lower confidence. Whenever it is increased, it is not able to detect anything in the image.

    # Draws bounding boxes
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            conf = box.conf[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert the processed frame back to bytes and send to client
    _, buffer = cv2.imencode(".jpg", frame)
    return Response(buffer.tobytes(), mimetype="image/jpeg")