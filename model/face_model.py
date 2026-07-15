from insightface.app import FaceAnalysis
class FaceModel :
    def __init__(self):
        self.app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        self.app.prepare(ctx_id=-1)
        print("Face Recognition Model Loaded Successfully.")
    def get_model(self):
        return self.app
face_model = FaceModel()
app = face_model.get_model()