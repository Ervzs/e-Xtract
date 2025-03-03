from flask import Blueprint, render_template, request, jsonify, session, Flask, Response, send_file, url_for, redirect
import os
import cv2
import numpy as np
from ultralytics import YOLO


extract_bp = Blueprint('extract', __name__) #initialize blueprint

#02.20.25 Ervzs removed static_folder and template_folder
#create_app() in blueprints/__init__.py already sets static_folder and template_folder for the whole app.
#No need to redefine it for each blueprint.



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

@extract_bp.route("/choose_mod")
def choose_model():
    '''
    This function is responsible for choosing the model to be used in YOLO.
    '''
    
    global model
    device = request.args.get('device', None)  # Get the device from the choose_device.html.

    if device == 'mobile':
        model = YOLO(r"models/image-proc/best.pt")  # Load smartphone model
    elif device == 'laptop':
        pass
    elif device == 'telecom':
        pass
    else:
        redirect(url_for('views.home'))

    # Redirect to the extract route
    return redirect(url_for('views.extract'))
    

def process_frame(frame, conf_threshold=0.6):
    '''
    This function takes an image frame, runs YOLO object detection, and draws bounding boxes with labels.
    '''
    results = model(frame, conf=0.6)  # Run YOLO on the frame which will return detected object with 60% confidence score.

    #Return value initialization
    detected_type = None  
    detected_model = None  
    detected_val_comps = [] 
    req_tools = []
    gen_instruction = None

    # Valuable components list
    val_comps = ['battery', 'camera', 'Vibrator Motor', 'screws', 'flex cables', 'Speaker', 'other-parts'] 
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # This extracts the bounding box.
            label = model.names[int(box.cls[0])]  # This extracts label. box.cls[0] is the class index, which is mapped to model.names to get the object’s name.
            conf = box.conf[0]  # This extracts the confidence score.
            
            # tatanggalin soon, for testing lang in passing detected ojects to variables
            detected_type = label

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) #This is the bounding box
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),  # The label (object name) and confidence score are drawn above the box.
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Responsible for detecting valuable components and ignores duplicates
            if label in val_comps:
                if label in detected_val_comps:
                    continue
                detected_val_comps.append(label)

    _, buffer = cv2.imencode(".jpg", frame)  # Converts the frame into JPG format

    #return values
    return ( 
        buffer.tobytes(), 
        detected_type if detected_type else "N/A",  
        detected_model if detected_model else "N/A",  
        detected_val_comps if detected_val_comps else ["N/A"],
        req_tools if req_tools else ["N/A"],
        gen_instruction if gen_instruction else "N/A"
    )

@extract_bp.route("/video_feed", methods=["POST"]) # route so functions in extract.html can access it
#HTTP responses are typically sent as text or binary data. Since images are binary, we must encode them into a transferable format like JPEG bytes.

def video_feed():
    file = request.files["frame"].read() # .read() converts it into raw binary data (bytes).
    npimg = np.frombuffer(file, np.uint8) # treats the binary data as an array of unsigned 8-bit integers (0–255), just like image pixels.
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR) # cv2.imdecode() converts the array into an actual image in OpenCV format.

    processed_frame, _, _ = process_frame(frame, conf_threshold=0.6)

    return Response(processed_frame, mimetype="image/jpeg") #Python processes the frame with YOLO & sends back a processed image
                                                             # It is returned to extract.html in the sendFrame(), line 95

@extract_bp.route("/process_image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify({"error": "No file found"}), 400

    # Read the uploaded file and convert it to an OpenCV image
    file = request.files["file"].read()
    npimg = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Resize the frame to the model's expected input size
    frame = cv2.resize(frame, (640, 640))

    # Process detection results including bounding box and labels
    processed_frame, detected_type, detected_model, detected_val_comps, req_tools, gen_instruction = process_frame(frame, conf_threshold=0.6)

    return jsonify({
        "device_image": processed_frame.decode("latin1"),  # Convert bytes to string for JSON (html will convert it back to bytes)
        "device_type": detected_type,  
        "device_model": detected_model,
        "val_comps": detected_val_comps,
        "req_tools": req_tools,
        "gen_instruction": gen_instruction
    })
