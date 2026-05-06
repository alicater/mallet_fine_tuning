import os
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "chroma_db") 

print("1. Loading documents...")
docs = []

# Load Method of Movement PDF
pdf_path = os.path.join(DATA_DIR, "Method_of_Movement.pdf")
if os.path.exists(pdf_path):
    docs.extend(PyPDFLoader(pdf_path).load())

# Load Steve Weiss Mallets CSV
csv_path = os.path.join(DATA_DIR, "marimba_mallets_dataset.csv")
if os.path.exists(csv_path):
    docs.extend(CSVLoader(csv_path).load())

# Load Marimba Markdown
md_path = os.path.join(DATA_DIR, "Marimba.md")
if os.path.exists(md_path):
    docs.extend(TextLoader(md_path, encoding="utf-8").load()) 

print(f"Loaded {len(docs)} document pages/rows.")

# Split text into chunks so they fit in the model's context window
print("2. Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=150)
chunks = text_splitter.split_documents(docs)

print("3. Generating embeddings and building Chroma DB...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory=DB_PATH
)

print(f"✅ Chroma vector database successfully built at {DB_PATH}")