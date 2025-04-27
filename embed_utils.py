from sentence_transformers import SentenceTransformer, models,util

import torch

def get_embedder():
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Load everything safely
    return model


def compute_similarity(resume_text, jd_text, embedder):
    resume_embedding = embedder.encode(resume_text, convert_to_tensor=True)
    jd_embedding = embedder.encode(jd_text, convert_to_tensor=True)
    similarity = util.cos_sim(resume_embedding, jd_embedding)
    return similarity.item()
