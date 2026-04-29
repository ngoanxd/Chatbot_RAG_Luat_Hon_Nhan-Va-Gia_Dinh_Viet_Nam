from data.loader import load_docs
from retriever.faiss_db import FaissDB

print(" Building FAISS index...")

docs = load_docs()
FaissDB(docs)  # sẽ tự save

print("Done! KHÔNG cần build lại nữa")