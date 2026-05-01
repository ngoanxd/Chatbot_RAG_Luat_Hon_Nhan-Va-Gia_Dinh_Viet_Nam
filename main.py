import warnings
import os
from transformers.utils import logging

logging.set_verbosity_error()

warnings.filterwarnings("ignore")

os.environ["LANGCHAIN_VERBOSE"] = "false"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


from data.loader import load_docs
from retriever.bm25 import BM25Retriever
from retriever.faiss_db import FaissDB
from retriever.hybrid import hybrid_search
from llm.model import get_llm
from llm.rewrite import rewrite_query_llm
from llm.analyze import analyze_context
import warnings
import time
from cache.cache_semantic import SemanticCache
from config import EMBED_MODEL,CACHE_PATH
from config import *
from langchain_community.embeddings import HuggingFaceEmbeddings

llm = get_llm()
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"}
    )

embeddings = get_embeddings()

def ui(role, text):
    if role == "user":
        print(f"\n👤 Bạn: {text}")
    else:
        print(f"\n🤖 Bot: {text}")


def main():
   
    print("\n==============================")
    print(" 🤖 CHATBOT LUẬT HÔN NHÂN ")
    print("==============================")

    # INIT CACHE
    cache = SemanticCache(
        embeddings_model=embeddings,
        path=CACHE_PATH,
        threshold=0.85
    )

    # LOAD DATA
    docs = load_docs()

    # INIT RETRIEVERS
    bm25 = BM25Retriever(docs)
    faiss = FaissDB(docs)

    while True:
        query = input("\n📝 Nhập câu hỏi (exit để thoát): ")
        ui("user", query)

        if query.lower().strip() == "exit":
            print("👋 Tạm biệt!")
            break

        # rewrite query
        re_query = rewrite_query_llm(query, llm, True)

        # =========================
        #  CACHE CHECK
        # =========================
        cached_answer = cache.search(re_query)

        if cached_answer is not None:
            ui("bot", f"(CACHE HIT)\n{cached_answer}")
            continue   #  KHÔNG lưu cache, KHÔNG gọi LLM

        # =========================
        # RETRIEVE CONTEXT
        # =========================
        context = hybrid_search(re_query, docs, bm25, faiss)

        ask_count = 0

        while True:

            check = analyze_context(re_query, context,llm)

            if not check["enough"]:
                if ask_count >= 2:
                    ui("bot", "Tôi sẽ trả lời dựa trên thông tin hiện có.")
                    check["enough"] = True
                else:
                    ui("bot", check["question_for_user"])

                    user_input = input("\n👤 Bạn: ")

                    if user_input.lower() == "exit":
                        return

                    ask_count += 1

                    re_query += (
                        " Câu hỏi gợi ý: " + check["question_for_user"] +
                        " Câu trả lời người dùng: " + user_input + " , "
                    )

                    re_query = rewrite_query_llm(re_query, llm, False)

                    cached_answer = cache.search(re_query)

                    if cached_answer is not None:
                        ui("bot", f"(CACHE HIT)\n{cached_answer}")
                        break

                    continue

            # =========================
            # LLM ANSWER
            # =========================
            answer = llm.invoke(f"""
            -Bạn là chatbot tư vấn pháp luật và cần độ chính xác cao, dựa vào context hãy trả lời query (câu hỏi) phía dưới.
            hãy suy luận thật kỹ context và query để trả lời cho chính xác.
            -Chỉ trả lời Tiếng Việt Nam, NGẮN GỌN và đúng trọng tâm và không suy diễn.

            Context:
            {context}

            Câu hỏi:
            {re_query}
            """)
            # =========================
            # SAVE CACHE (CHỈ CACHE MISS)
            # =========================
            cache.add(re_query, answer)

            ui("bot", answer)

            print("\n Kết thúc phiên hỏi luật")
            break


if __name__ == "__main__":
    main()
