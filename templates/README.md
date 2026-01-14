

# **Gemini RAG Policy Chatbot**

A **secure, enterprise-grade AI assistant** that answers questions on company policy documents using **Google Gemini**, **RAG (Retrieval-Augmented Generation)**, **FAISS**, **Flask**, **JWT**, and **HashiCorp Vault**.

This project demonstrates how large organizations can safely use LLMs **without exposing confidential data**.



## What This System Does

* Reads multiple company policy PDFs
* Converts them into searchable embeddings
* Retrieves only the relevant chunks for each question
* Uses Gemini LLM to generate grounded answers
* Protects secrets using Vault
* Secures access using JWT

No documents are ever sent to Gemini in full.
No data is stored or trained by the LLM.

---


## How It Works (Interactive Flow)

1. User logs in → receives JWT token
2. User asks a question
3. Flask validates JWT
4. Query → Vector Search (FAISS)
5. Relevant document chunks retrieved
6. Gemini API key fetched from Vault
7. Gemini receives:
      - User question
      - Retrieved policy chunks
8. Gemini generates answer
9. Response returned to user


##  Security Model

| Layer       | Protection                                  |
| ----------- | ------------------------------------------- |
| JWT         | Only authenticated users can query          |
| Vault       | Gemini API key is encrypted & never in code |
| RAG         | Gemini never sees full documents            |
| FAISS       | Company data stored locally                 |
| No training | Gemini does not learn your data             |
| Audit-ready | All access can be logged                    |

This follows the same model used by:

* Microsoft Copilot
* Google Vertex AI
* Salesforce Einstein
* Enterprise AI copilots


##  Project Structure

rag_gemini_chatbot/
│
├── app.py                # Flask API + UI
├── rag_chat.py           # RAG orchestration
├── vector_store.py       # FAISS + embeddings
├── ingest.py             # PDF loading & chunking
├── vault_client.py       # Secure secret retrieval
├── documents/            # Company PDFs
│     └── policy.pdf
├── templates/
│     └── chat.html       # Web UI
├── static/
│     └── style.css
├── Dockerfile
└── README.md

##  How to Run

### Start Vault

```bash
vault server -dev
export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="s.xxxxx"
vault kv put secret/gemini api_key="YOUR_GEMINI_KEY"
```

---

###  Install dependencies

```bash
pip install flask google-genai faiss-cpu pypdf numpy hvac flask-jwt-extended
```



### Build vector database

```bash
python -c "from ingest import load_all_pdfs, chunk_text; from vector_store import create_vector_db; text=load_all_pdfs(); chunks=chunk_text(text); create_vector_db(chunks)"
```

---

###  Run application

```bash
python app.py
```

Open:

```
http://localhost:8000
```

Login:

```
admin / admin123
```



## Docker Support

```bash
docker build -t gemini-rag .
docker run -p 8000:8000 gemini-rag
```



## Why This Matters

This project demonstrates:

> **How to use LLMs in a bank, enterprise, or government environment without leaking data**

It solves:

* Data privacy
* Compliance
* Security
* Vendor lock-in
* Hallucinations

Using:

* RAG
* Vault
* JWT
* Vector databases

---



