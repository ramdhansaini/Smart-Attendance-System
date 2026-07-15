from flask import Flask, render_template, request, redirect
import os
from model.generate_embeddings import generate_embeddings
from model.recognize import FaceRecognizer
from utils.file_handler import (save_uploaded_images, save_temp_image, delete_temp_file)
from utils.image_handler import save_webcam_image
from utils.attendance import (mark_attendance, get_attendance)
app = Flask(__name__)
recognizer = FaceRecognizer()
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/capture")
def capture():
    return render_template("capture.html")
@app.route("/attendance")
def attendance():
    records = get_attendance()
    return render_template("attendance.html", records=records)
@app.route("/register", methods=["POST"])
def register():
    student_name = request.form["student_name"]
    images = request.files.getlist("images")
    save_uploaded_images(student_name, images)
    generate_embeddings()
    return redirect("/")
@app.route("/recognize", methods=["POST"])
def recognize():
    image_path = None
    uploaded_image = request.files.get("image")
    if uploaded_image and uploaded_image.filename != "":
        image_path = save_temp_image(uploaded_image)
    else:
        captured = request.form.get("captured_image")
        if captured:
            image_path = save_webcam_image(captured)
    if image_path is None:
        return render_template(
            "result.html",
            status=False,
            message="No image selected."
        )
    result = recognizer.recognize(image_path)
    delete_temp_file(image_path)
    if result["status"]:
        mark_attendance(result["student"])
    return render_template(
        "result.html",
        status=result["status"],
        student=result.get("student"),
        similarity=result.get("similarity"),
        message=result["message"]
    )
if __name__ == "__main__":
    app.run(debug=True)