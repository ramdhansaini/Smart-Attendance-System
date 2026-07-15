import os
import cv2
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from model.face_model import app
EMBEDDINGS_PATH = "data/embeddings.pkl"
class FaceRecognizer :
    def __init__(self) :
        if not os.path.exists(EMBEDDINGS_PATH):
            raise FileNotFoundError("embeddings.pkl not found.\n" "Run generate_embeddings.py first")
        with open(EMBEDDINGS_PATH, "rb") as file :
            self.embeddings = pickle.load(file)
    def recognize(self, image_path, threshold=0.60):
        image = cv2.imread(image_path)
        if image is None :
            return {
                "status" : False,
                "message" : "Image cannot be read."
            }
        faces = app.get(image)
        if len(faces) == 0 :
            return {
                "status" : False,
                "message" : "No face detected."
            }
        unknown_embedding = faces[0].embedding
        best_score = -1
        best_student = None
        for student, stored_embeddings in self.embeddings.items():
            for stored_embedding in stored_embeddings:
                score = cosine_similarity(unknown_embedding.reshape(1, -1),
                                          stored_embedding.reshape(1, -1))[0][0]
            if score>best_score :
                best_score = score
                best_student = student
                print("Best Student:", best_student)
                print("Best Score:", best_score)
                print("Threshold:", threshold)
            if best_score >= threshold :
                return {
                    "status" : True,
                    "student" : best_student,
                    "similarity" : round(float(best_score), 4),
                    "message" : "Face Matched"
                }
            return {
                    "status" : False,
                    "student" : None,
                    "similarity" : round(float(best_score), 4),
                    "message" : "Person Not Registered"
                }
if __name__ == "__main__":

    recognizer = FaceRecognizer()

    result = recognizer.recognize(
        "static/uploads/test.jpg"
    )

    print(result)