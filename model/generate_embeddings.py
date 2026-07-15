import os
import cv2
import pickle
from model.face_model import app
DATASET_PATH = "dataset"
OUTPUT_PATH = "data/embeddings.pkl"
def generate_embeddings() :
    embeddings = {}
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset folder '{DATASET_PATH}' not found.")
        exit()
    for student_name in os.listdir(DATASET_PATH):
        student_folder = os.path.join(DATASET_PATH, student_name)
        if not os.path.isdir(student_folder):
            continue
        print(f"\n Processing {student_name}")
        student_embeddings = []
        for image_name in os.listdir(student_folder):
            image_path = os.path.join(student_folder, image_name)
            image = cv2.imread(image_path)
            if image is None :
                print(f"cannot read {image_name}")
            faces = app.get(image)
            if len(faces) == 0:
                print(f"No face found in {image_name}")
                continue
            embedding = faces[0].embedding
            student_embeddings.append(embedding)
            print(f"Embedding created : {image_name}")
        if len(student_embeddings) > 0 :
            embeddings[student_name] = student_embeddings
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "wb") as file :
        pickle.dump(embeddings, file)
    print("\n===================================")
    print("Embeddings Generated Successfully")
    print(f"Total Students : {len(embeddings)}")
    print(f"Saved to : {OUTPUT_PATH}")
    print("===================================")
if __name__ == "__main__":
    generate_embeddings()