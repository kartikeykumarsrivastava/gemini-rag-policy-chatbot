from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from rag_chat import ask_gemini
import datetime

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"   # store in env in prod
jwt = JWTManager(app)

# --- Login ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "admin" and data["password"] == "admin123":
        token = create_access_token(identity="admin", expires_delta=datetime.timedelta(hours=1))
        return jsonify(access_token=token)
    return jsonify({"error": "Invalid credentials"}), 401

# --- UI ---
@app.route("/")
def home():
    return render_template("chat.html")

# --- Secure Chat ---
@app.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    query = request.json["message"]
    answer = ask_gemini(query)
    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
