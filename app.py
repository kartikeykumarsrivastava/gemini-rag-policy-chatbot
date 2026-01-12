from flask import Flask, request, jsonify, render_template
from rag_chat import ask_gemini

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
