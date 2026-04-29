from data.loader import load_docs
from retriever.bm25 import BM25Retriever
from retriever.faiss_db import FaissDB
from retriever.hybrid import hybrid_search
from llm.model import llm
from llm.rewrite import rewrite_query_llm
from llm.analyze import analyze_context
import warnings
import time

warnings.filterwarnings("ignore")

def ui(role, text):
    if role == "user":
        print(f"\n👤 Bạn: {text}")
    else:
        print(f"\n🤖 Bot: {text}")


def main():
    print("\n==============================")
    print(" 🤖 CHATBOT LUẬT HÔN NHÂN ")
    print("==============================")

    docs = load_docs()

    bm25 = BM25Retriever(docs)

    faiss = FaissDB()

    while True:
        query = input("\n👉 Nhập câu hỏi (exit để thoát): ")

        if query.lower() == "exit":
            print("👋 Tạm biệt!")
            break
        
        ui("user", query)

        print(f"  Đang tra cứu câu hỏi...")
        # =====================
        # 2. Retrieve context
        # =====================
        t0 = time.perf_counter()
        re_query,context = hybrid_search(query, docs, bm25, faiss)

        ask_count = 0

        while True:
            # =====================
            # 3. Check đủ info chưa
            # =====================
            t0 = time.perf_counter()
            check = analyze_context(re_query, context)
            # =====================
            # 4. Nếu thiếu → hỏi lại
            # =====================
            if not check["enough"]:
                
                if ask_count >= 2:
                    ui("bot", "Tôi sẽ trả lời dựa trên thông tin hiện có.")
                    check["enough"]=True
                else:
                    ui("bot", check["question_for_user"])
                
                    user_input = input("\n 👤 Bạn: ")
                    print(f"  Đang tra cứu câu hỏi...")
                    if user_input.lower() == "exit":
                        print("👋 Tạm biệt!")
                        return

                    ask_count += 1

                    # append hội thoại
                    re_query += (
                        " Câu hỏi gợi ý: " + check["question_for_user"] +
                        " Câu trả lời người dùng: " + user_input + " , "
                    )

                    # rewrite lại query
                    re_query = rewrite_query_llm(re_query, llm, False)

                    continue

            # =====================
            # 5. Đủ → trả lời
            # =====================
            answer = llm.invoke(f"""
            -Bạn là chatbot tư vấn pháp luật và cần độ chính xác cao, dựa vào context hãy trả lời query (câu hỏi) phía dưới.
            hãy suy luận thật kỹ context và query để trả lời cho chính xác.
            -Chỉ trả lời Tiếng Việt Nam, NGẮN GỌN và đúng trọng tâm và không suy diễn.

            Context:
            {context}

            Câu hỏi:
            {re_query}
            """)
    
            print(f"\n Câu trả lời: {answer}\n Kết thúc phiên tra cứu pháp luật cám ơn bạn! ")
           
            break


if __name__ == "__main__":
    main()