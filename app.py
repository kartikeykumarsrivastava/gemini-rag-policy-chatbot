from flask import Flask, request, jsonify, render_template
from rag_chat import ask_gemini

import os

if not os.path.exists("policy.index"):
    from ingest import load_pdf, chunk_text
    from vector_store import create_vector_db
    text = load_pdf("EN-collective-agreement.pdf")
    chunks = chunk_text(text)
    create_vector_db(chunks)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("message")

    answer = ask_gemini(user_query)
    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
