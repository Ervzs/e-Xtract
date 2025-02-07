from flask import Blueprint, render_template, request, jsonify, session, Flask, Response
import os
import google.generativeai as genai 
import cv2
from ultralytics import YOLO


extract_bp = Blueprint('extract', __name__, static_folder='static', template_folder='templates') #initialize blueprint

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = YOLO(r"models/image-proc/best.pt")  # Load YOLO model
cap = cv2.VideoCapture(0)  # Open webcam

@extract_bp.route("/extract")
def extract():
    return render_template("extract.html")

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, conf=0.6)  # Run YOLO on the frame

        #For manually getting the bounding box and Class labels. Will be used in further development when manipulating the detected object.
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
                label = model.names[int(box.cls[0])]  # Get class label
                conf = box.conf[0]  # Get confidence score

                # Draw bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        
        # Encode frame for streaming
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@extract_bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

