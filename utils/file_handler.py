import os
from werkzeug.utils import secure_filename
DATASET_FOLDER = "dataset"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS ={"jpg", "jpeg", "png"}
def allowed_file(filename):
    return("." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS)
def create_student_folder(student_name) :
    folder_path = os.path.join(DATASET_FOLDER, student_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path
def save_uploaded_images(student_name, image_files):
    folder = create_student_folder(student_name)
    saved_files = []
    image_number = 1
    for image in image_files :
        if image and allowed_file(image.filename):
            extension = image.filename.rsplit(".", 1)[1].lower()
            filename = f"{image_number}.{extension}"
            save_path = os.path.join(folder, filename)
            image.save(save_path)
            saved_files.append(save_path)
            image_number += 1
    return saved_files
def save_temp_image(image):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(image.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(path)
    return path
def delete_temp_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)