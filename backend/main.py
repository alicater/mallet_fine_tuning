from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_cpp import Llama
import os
from langchain_huggingface import HuggingFaceEmbeddings
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
    n_threads=8,
    n_gpu_layers=-1 # comment this out if it ends up messing with windows
)

print("Loading Chroma Vector Database...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

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
        return jsonify({"error": "No question was provided."}), 400

    # Searches Chroma for the answer in our data
    retrieved_docs = retriever.invoke(question)
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # Injects that context into the prompt
    prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
You are a master percussion educator and equipment expert. Answer the user's question clearly and practically based on the provided context.
Question: {question}

### Input:
Context: {context_text}

### Response:
"""

    response = llm(
        prompt,
        max_tokens=350,
        temperature=0.2, # keep temperature very low to keep relying on facts/data given
        stop=["### Instruction:", "### Input:"] 
    )

    answer = response["choices"][0]["text"].strip()

    return jsonify({
        "question": question,
        "answer": answer,
        "sources_used": [doc.metadata.get('source', 'Unknown') for doc in retrieved_docs]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)