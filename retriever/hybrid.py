import re
from sentence_transformers import CrossEncoder
from config import *
from llm.rewrite import rewrite_query_llm
from llm.model import llm
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device hybird {device}")

cross_encoder = CrossEncoder(RERANK_MODEL,device='cpu')

def extract_all_dieu(docs, meta=True):
    """
    Trích xuất tất cả số Điều từ docs

    Args:
        docs: List[Document]
        meta: True → chỉ lấy từ metadata (NHANH)
              False → lấy thêm từ content (CHẬM hơn)

    Returns:
        set[int]
    """
    all_dieu = set()

    for doc in docs:
        # 1. Lấy từ metadata (ưu tiên)
        dieu = doc.metadata.get("dieu")
        if dieu is not None:
            all_dieu.add(dieu)

        # 2. Nếu chỉ cần metadata → bỏ qua content
        if meta:
            continue

        content = doc.page_content

        # Điều 75
        matches = re.findall(r"Điều\s*(\d+)", content, re.IGNORECASE)
        all_dieu.update(map(int, matches))

        # điều 60,61 và 64
        clusters = re.findall(
            r"điều\s*((?:\d+\s*(?:,|và)\s*)+\d+)",
            content,
            re.IGNORECASE
        )

        for c in clusters:
            nums = re.findall(r"\d+", c)
            all_dieu.update(map(int, nums))

    return all_dieu

def rerank(query, docs, top_k):
    if not docs:
        return []

    pairs = [(query, d.page_content) for d in docs]

    scores = cross_encoder.predict(
        pairs,
        batch_size=16   #tăng tốc GPU
    )

    ranked = list(zip(docs, scores))
    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked[:top_k]


def hybrid_search(query, docs, bm25, faiss, k_bm25=3, k_faiss=15, k_rerank=6):
    """
    Pipeline:
    1. Rewrite query
    2. BM25 + FAISS
    3. Merge
    4. Extract Điều
    5. Filter docs
    6. Rerank
    7. Build context
    """

    # =====================
    # 1. Rewrite query
    # =====================
    re_query = rewrite_query_llm(query, llm, first=True)

    # =====================
    # 2. Retrieve
    # =====================
    bm25_docs = bm25.search(re_query, k_bm25)
    faiss_docs = faiss.search(re_query, k_faiss)

    # =====================
    # 3. Merge candidates
    # =====================
    candidates = bm25_docs + faiss_docs

    # =====================
    # 4. Extract Điều
    # =====================
    dieu_set = extract_all_dieu(candidates, meta=True)

    if not dieu_set:
        return re_query, ""

    # =====================
    # 5. Filter docs theo Điều
    # =====================
    filtered_docs = [
        doc for doc in docs if doc.metadata.get("dieu") in dieu_set
    ]

    if not filtered_docs:
        return re_query, ""

    # =====================
    # 6. Rerank (DÙNG re_query)
    # =====================
    reranked = rerank(
        query=re_query,
        docs=filtered_docs,
        top_k=k_rerank
    )

    reranked_docs = [doc for doc, _ in reranked]

    # =====================
    # 7. Expand thêm Điều từ content (OPTIONAL)
    # =====================
    expanded_dieu = extract_all_dieu(reranked_docs, meta=False)

    final_docs = [
        doc for doc in docs if doc.metadata.get("dieu") in expanded_dieu
    ]

    # =====================
    # 8. Build context (NHANH hơn)
    # =====================
    context = "\n\n".join(
        doc.page_content.strip() for doc in final_docs
    )

    return re_query, context