import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
def cosine_similarity_score(embedding1, embedding2):
    score = cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1))[0][0]
    return float(score)
def euclidean_distance(embedding1, embedding2):
    return float(np.linalg.norm(embedding1 - embedding2))