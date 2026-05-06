from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_cpp import Llama
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "marimba_expert_v1.gguf")

print("Loading model...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8
)
print("Model loaded successfully.")


@app.route("/")
def home():
    return jsonify({
        "message": "Marimba Expert backend is running"
    })


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question was provided"}), 400

    prompt = f"""
You are a helpful marimba expert. Answer questions about marimba technique, practice, music, performance, and setup.

Question: {question}

Answer:
"""

    response = llm(
        prompt,
        max_tokens=300,
        temperature=0.7,
        stop=["Question:"]
    )

    answer = response["choices"][0]["text"].strip()

    return jsonify({
        "question": question,
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)