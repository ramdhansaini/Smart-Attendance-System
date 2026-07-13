import os
import cv2
import re
import base64
import pickle
import face_recognition
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
# -------------------------------
# Face Capture Function
# -------------------------------
def capture_face(user_id: str, user_name: str) -> None:
    cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    count = 0
    os.makedirs(f"dataset/{user_id}", exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.imwrite(f"dataset/{user_id}/{user_name}_{count}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Capturing Faces', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
            break

    cam.release()
    cv2.destroyAllWindows()

# -------------------------------
# Flask Routes
# -------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['id']
        user_name = request.form['name']
        
        # Capture face images
        capture_face(user_id, user_name)
        
        # Update encodings
        encode_faces()
        
        return "Face registered successfully!"
    return render_template('registerstudent.html')

# Route for AJAX capture (if using webcam + JS)
@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    image_data = re.sub('^data:image/.+;base64,', '', data['image'])
    image_bytes = base64.b64decode(image_data)

    os.makedirs("dataset", exist_ok=True)
    filename = f"dataset/student_{len(os.listdir('dataset'))+1}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)

    return jsonify({"message": "Face captured and saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
