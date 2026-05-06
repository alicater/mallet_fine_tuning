from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_cpp import Llama
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "marimba_expert_v1.gguf")
DB_PATH = os.path.join(BASE_DIR, "chroma_db") 

print("Loading model from:", MODEL_PATH)


llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8
)

print("Loading Chroma Vector Database...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load the existing database from the directory
vectorstore = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("✅ Backend fully loaded and ready.")
@app.route("/")
def home():
    return jsonify({
        "message": "Marimba Expert backend is running"
    })


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question", "")

    if not question.strip():
        return jsonify({
            "error": "No question was provided."
        }), 400

    prompt = f"""
You are a helpful marimba and mallet percussion expert.

Answer the user's question clearly and practically.
Focus on technique, practice advice, tone quality, rhythm, grip, repertoire, and performance.

User question:
{question}

Answer:
"""

    response = llm(
        prompt,
        max_tokens=350,
        temperature=0.7,
        stop=["User question:"]
    )

    answer = response["choices"][0]["text"].strip()

    return jsonify({
        "question": question,
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)