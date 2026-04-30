import re
from rank_bm25 import BM25Okapi

def tokenize(text):
    text = text.lower().split()
    tokens = [re.sub(r"[^\w]", "", w) for w in text]
    tokens = [w for w in tokens if w]
    stopwords = {'là','của','và','theo','được','thì'}
    return [w for w in tokens if w not in stopwords]


class BM25Retriever:
    def __init__(self, docs):
        self.docs = docs
        self.corpus = [tokenize(d.page_content) for d in docs]
        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query, k):
        tokens = tokenize(query)
        scores = self.bm25.get_scores(tokens)

        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.docs[i] for i in top_idx]
