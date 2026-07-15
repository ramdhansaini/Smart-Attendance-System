import os
import cv2
import base64
import numpy as np
UPLOAD_FOLDER = "static/uploads"
def read_image(image_path):
    image = cv2.imread(image_path)
    return image
def resize_image(image, width=640):
    height = int(image.shape[0] * (width/image.shape[1]))
    resized = cv2.resize(image, (width, height))
    return resized
def is_valid_image(image):
    return image is not None
def base64_to_image(base64_string):
    if "," in base64_string :
        base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image
def save_webcam_image(base64_string, filename="capture.jpg"):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    image = base64_to_image(base64_string)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    cv2.imwrite(save_path, image)
    return save_path
