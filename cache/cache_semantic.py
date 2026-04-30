import os
import json
from sklearn.metrics.pairwise import cosine_similarity

class SemanticCache:
    def __init__(self, embeddings_model, path, threshold=0.85):
        self.embeddings = embeddings_model
        self.threshold = threshold
        self.path = path

        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_cache(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def add(self, query_text, answer_text):
        vec = self.embeddings.embed_query(query_text)

        self.cache.append({
            "text": query_text,
            "vector": vec,
            "answer": str(answer_text)
        })

        self.save_cache()

    def search(self, query_text):
        if len(self.cache) == 0:
            return None

        query_vec = self.embeddings.embed_query(query_text)

        best_score = -1
        best_answer = None

        for item in self.cache:
            score = cosine_similarity(
                [query_vec],
                [item["vector"]]
            )[0][0]

            if score > best_score:
                best_score = score
                best_answer = item["answer"]

        if best_score >= self.threshold:
            return best_answer

        return None