from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight & fast

def get_similar_docs(doc_id, db, top_n=5):
    all_docs = list(db.documents.find())
    
    texts = [doc['content'] for doc in all_docs]
    ids = [str(doc['_id']) for doc in all_docs]

    embeddings = model.encode(texts)

    try:
        target_index = ids.index(doc_id)
    except ValueError:
        return []

    target_embedding = embeddings[target_index].reshape(1, -1)
    similarities = cosine_similarity(target_embedding, embeddings)[0]

    sorted_indices = similarities.argsort()[::-1]
    top_matches = [i for i in sorted_indices if i != target_index][:top_n]

    results = []
    for i in top_matches:
        doc = all_docs[i]
        results.append({
            "filename": doc["filename"],
            "s3_url": doc["s3_url"],
            "tags": doc["tags"],
            "score": float(similarities[i])
        })

    return results
