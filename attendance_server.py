from flask import Flask, request, jsonify
import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis
import datetime
import base64
import json

app = Flask(__name__)

# Initialize RetinaFace
face_analyzer = FaceAnalysis(name='buffalo_l')
face_analyzer.prepare(ctx_id=0, det_size=(640, 640))

# Configuration
dataset_path = "Dataset/"
known_faces = {}  # Dictionary to store embeddings with names
threshold = 0.3  # Adjust similarity threshold as needed
attendance_log = "attendance_log.csv"  # File to log attendance

# Load dataset of known faces
def load_face_database():
    known_faces = {}
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset folder not found: {dataset_path}")
        return known_faces
    
    for person in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person)
        
        if not os.path.isdir(person_path):
            continue
        
        for filename in os.listdir(person_path):
            img_path = os.path.join(person_path, filename)
            
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            img = cv2.imread(img_path)
            if img is None:
                print(f"⚠ Corrupt or unreadable: {filename}")
                continue
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            faces = face_analyzer.get(img)
            
            if len(faces) > 0:
                embedding = faces[0].normed_embedding
                known_faces[person] = embedding
    
    print(f"✅ Loaded {len(known_faces)} known faces.")
    return known_faces

# Process image and track attendance
def process_attendance(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = face_analyzer.get(image_rgb)
    
    present_students = []
    
    for face in faces:
        x1, y1, x2, y2 = map(int, face.bbox)
        embedding = face.normed_embedding
        
        best_match = "Unknown"
        best_score = threshold
        
        # Compare with known faces
        for name, known_embedding in known_faces.items():
            similarity = np.dot(embedding, known_embedding)
            
            if similarity > best_score:
                best_score = similarity
                best_match = name
        
        # Add to attendance results
        if best_match != "Unknown":
            present_students.append({
                "name": best_match,
                "confidence": round(float(best_score) * 100, 2)
            })
            
            # Log attendance to file
            log_attendance(best_match)
        
        # Draw bounding box
        color = (0, 255, 0) if best_match != "Unknown" else (0, 0, 255)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, best_match, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Save the processed image
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"processed_{timestamp}.jpg"
    cv2.imwrite(output_path, image)
    
    return present_students, output_path

# Log attendance to CSV file
def log_attendance(name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Create log file if it doesn't exist
    if not os.path.exists(attendance_log):
        with open(attendance_log, 'w') as f:
            f.write("Name,Date,Time\n")
    
    # Log the attendance
    with open(attendance_log, 'a') as f:
        f.write(f"{name},{date},{timestamp}\n")

# API endpoint to receive images for attendance tracking
@app.route('/attendance', methods=['POST'])
def track_attendance():
    if 'image' not in request.files:
        # Check if the image is sent as base64 in JSON
        if request.json and 'image' in request.json:
            try:
                # Decode base64 image
                image_data = base64.b64decode(request.json['image'])
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as e:
                return jsonify({'error': f'Failed to decode image: {str(e)}'}), 400
        else:
            return jsonify({'error': 'No image provided'}), 400
    else:
        # Get image from form data
        image_file = request.files['image']
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return jsonify({'error': 'Invalid image'}), 400
    
    # Process the image for attendance
    present_students, image_path = process_attendance(image)
    
    # Create response data
    response_data = {
        'success': True,
        'message': f'Attendance tracked for {len(present_students)} students',
        'present': present_students,
        'processed_image': image_path,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Log response format to terminal for debugging
    print("\n===== RESPONSE DATA FORMAT =====")
    print(json.dumps(response_data, indent=4))
    print("================================\n")
    
    # Return the results
    return jsonify(response_data)

# API endpoint to check server status
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'online',
        'known_faces': len(known_faces),
        'server_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    # Load the face database when server starts
    known_faces = load_face_database()
    
    # Run the Flask app (accessible from other devices on the network)
    app.run(host='0.0.0.0', port=5000, debug=True)
