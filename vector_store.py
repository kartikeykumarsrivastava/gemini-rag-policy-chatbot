from google import genai
import faiss
import numpy as np
import pickle
import os

client = genai.Client(api_key=os.getenv("AIzaSyApk7AAPfTheG9OGcJ0RKNwPKkch5cuTLQ"))

EMBEDDING_MODEL = "models/text-embedding-004"

def embed_text(texts):
    vectors = []
    for text in texts:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        vectors.append(response.embeddings[0].values)

    return np.array(vectors).astype("float32")

def create_vector_db(chunks):
    vectors = embed_text(chunks)

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    faiss.write_index(index, "policy.index")

    print("Vector DB created")
