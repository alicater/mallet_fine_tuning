import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

print("Waking up embeddings and connecting to Chroma...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
print(f"Total documents in database: {db._collection.count()}")

test_query = "What is the proper mallet placement for a Stevens grip interval change?"

print(f"\n🔍 Searching for: '{test_query}'\n")

# returns the chunks and mathematical distance from the query
# for Chroma's default settings, a lower score is a closer match!
results = db.similarity_search_with_score(test_query, k=4)

for i, (doc, score) in enumerate(results):
    print(f"=== Match {i+1} | Distance Score: {score:.4f} ===")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
    print(f"Text: {doc.page_content.strip()[:300]}...\n")