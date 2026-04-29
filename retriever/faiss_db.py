import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import *

class FaissDB:
    def __init__(self, docs=None):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBED_MODEL,
            model_kwargs={"device": "cpu"}
        )

        if os.path.exists(FAISS_PATH):
            self.db = FAISS.load_local(
                FAISS_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            print("Chưa có FAISS → đang build...")
            self.db = FAISS.from_documents(docs, self.embeddings)
            self.db.save_local(FAISS_PATH)

    def search(self, query, k):
        return self.db.similarity_search(query, k=k)