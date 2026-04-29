DATA_PATH = r"D:\CHATBOT_RAG\data-2\luat_hon_nhan"

CHUNK_SIZE = 2100
CHUNK_OVERLAP = 100

K_BM25 = 3
K_FAISS = 10
K_RERANK = 5

EMBED_MODEL = "BAAI/bge-m3"
RERANK_MODEL = "BAAI/bge-reranker-v2-m3"
LLM_MODEL = "qwen3"

FAISS_PATH = "faiss_store"
CACHE_PATH = "cache.json"