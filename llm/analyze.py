from utils.json_utils import safe_json_parse
from llm.model import llm
# 🔹 analyze (prompt viết cứng cho mistral)
def analyze_context(query, context):
    result = llm.invoke(f"""
    Bạn là chuyên gia pháp luật.

    NHIỆM VỤ:
    - KHÔNG trả lời câu hỏi
    - CHỈ kiểm tra query có đủ thông tin để dùng context tư vấn chưa, nếu query chứa nhiều thông tin mà chưa cho ra truy vấn cụ chính xác context thì enough=True.
                            
    TIÊU CHÍ:
        - Nếu thiếu thông tin từ query  → enough = False
        - Nếu query đủ để trả lời context → enough = True ,question_for_user= None
                            
    QUY TẮC:
    - Chỉ trả JSON
    - KHÔNG giải thích
    - KHÔNG thêm chữ nào ngoài JSON
    - KHÔNG xuống dòng trước hoặc sau JSON
    - JSON phải hợp lệ 100%
                        
    - Chỉ hỏi 1 câu duy nhất
    - Câu hỏi phải NGẮN, RÕ, CỤ THỂ
    - Hỏi đúng vào phần THIẾU trong query
    - Câu hỏi phải giúp trả lời chính xác hơn
    - KHÔNG hỏi chung chung (ví dụ: "bạn nói rõ hơn")
                        
   FORMAT:
    {{
    "enough": True/False,
    "question_for_user": "hỏi user Hỏi đúng vào phần THIẾU trong query"
    }}

    Context:
    {context}

    Query:
    {query}

    """)

    return safe_json_parse(result)


