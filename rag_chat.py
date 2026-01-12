from google import genai
import faiss
import pickle
import numpy as np
import os

client = genai.Client(api_key=os.getenv("API_KI"))

LLM_MODEL = "models/gemini-pro-latest"
EMBED_MODEL = "models/text-embedding-004"

index = faiss.read_index("policy.index")
chunks = pickle.load(open("chunks.pkl", "rb"))

def embed_query(query):
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=query
    )
    return np.array(response.embeddings[0].values).astype("float32")

def retrieve_context(query, k=3):
    q_vec = embed_query(query).reshape(1, -1)
    _, I = index.search(q_vec, k)
    return "\n".join([chunks[i] for i in I[0]])

def ask_gemini(query):
    context = retrieve_context(query)

    prompt = f"""
    You are a company policy assistant.
    Use ONLY the provided context.

    CONTEXT:
    {context}

    QUESTION:
    {query}
    """

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    return response.text
