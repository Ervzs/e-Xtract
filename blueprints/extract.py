from flask import Blueprint, render_template, request, jsonify, session, Flask, Response, send_file
import os
import cv2
import numpy as np
from ultralytics import YOLO


extract_bp = Blueprint('extract', __name__) #initialize blueprint

#02.20.25 Ervzs removed static_folder and template_folder
#create_app() in blueprints/__init__.py already sets static_folder and template_folder for the whole app.
#No need to redefine it for each blueprint.


model = YOLO(r"models/image-proc/best.pt")  # Load YOLO model

'''
Use only for local servers
cap = cv2.VideoCapture(0)  # Open webcam
'''


'''
This python file is responsible for processing the frames from a video or images using the YOLO model. It has three functions
1. process_frame() - This function process a single frame and returns an encoded image.
2. video_feed() - Handles video frames uploaded via HTTP POST request and returns a processed image.
3. process_image() - Handles uploaded images, processes them using YOLO, and returns both image and detected object.
'''


def process_frame(frame):
    results = model(frame, conf=0.6)  # Run YOLO on the frame which will return detected object with 60% confidence score.

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0]) # This extracts the bounding box.
            label = model.names[int(box.cls[0])] # This extracts label. box.cls[0] is the class index, which is mapped to model.names to get the object’s name.
            conf = box.conf[0] # This extracts the confidence score.

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) #This is the bounding box
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), # The label (object name) and confidence score are drawn above the box.
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, buffer = cv2.imencode(".jpg", frame) # Converts the frame into JPG format
    return buffer.tobytes() # The frame is returned as bytes


'''
 HTTP responses are typically sent as text or binary data. Since images are binary, we must encode them into a transferable format like JPEG bytes.
'''

@extract_bp.route("/video_feed", methods=["POST"]) # route so functions in extract.html can access it.
def video_feed():
    file = request.files["frame"].read() # .read() converts it into raw binary data (bytes).
    npimg = np.frombuffer(file, np.uint8) # treats the binary data as an array of unsigned 8-bit integers (0–255), just like image pixels.
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR) # cv2.imdecode() converts the array into an actual image in OpenCV format.

    results = model(frame, conf=0.6)  # Run YOLO on the frame

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            conf = box.conf[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), #displays the details about the object detected
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, buffer = cv2.imencode(".jpg", frame)
    return Response(buffer.tobytes(), mimetype="image/jpeg") #Python processes the frame with YOLO & sends back a processed image
                                                             # It is returned to extract.html in the sendFrame(), line 95


@extract_bp.route("/process_image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify({"error": "No file found"}), 400

    # read the uploaded file and convert it to an OpenCV image
    file = request.files["file"].read()
    npimg = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Resized the frame to the model's expected input size
    frame = cv2.resize(frame, (640, 640))

    # vriables that will store the detected object information
    detected_type = None
    detected_model = None # di pa nagamit
    
    # contains the detected objects by YOLO 
    results = model(frame, conf=0.1)

    # process detection results including bounding box and label
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            detected_type = label
            conf = box.conf[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert the processed frame back to bytes and send to client
    _, buffer = cv2.imencode(".jpg", frame)
    frame_bytes = buffer.tobytes()
    
    # changed return value from Response to jsonify because Response only returns the image and not the detected object type which is a string
    return jsonify({
        "device_image": frame_bytes.decode("latin1"),  # Convert bytes to string for JSON
        "device_type": detected_type,  # Return the detected object type
        "device_model": detected_model  # Return the detected
    })