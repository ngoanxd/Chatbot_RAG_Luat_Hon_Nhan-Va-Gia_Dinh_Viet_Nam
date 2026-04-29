def rewrite_query_llm(query, llm,first=True):
    if first:
        prompt=f"""
          Chuẩn hóa câu hỏi sau về luật hôn nhân & gia đình (sửa chính tả, ngữ pháp, làm rõ nghĩa).
            Yêu cầu: Giữ nguyên ý, KHÔNG để dấu kết thúc câu, CHỈ trả về duy nhất câu NGẮN GỌN nhất, không giải thích.
            Câu hỏi: {query}

        """
    else: 
        prompt = f"""
        Bạn là hệ thống chuẩn hóa câu hỏi pháp luật Hôn nhân và Gia đình.

        NHIỆM VỤ:
        - Từ hội thoại gồm: câu hỏi ban đầu + câu hỏi gợi ý + câu trả lời của người dùng
        - Hãy suy ra nhu cầu đầy đủ của người dùng (query).

        QUY TẮC BẮT BUỘC:
        - Ưu tiên thông tin ở câu trả lời của người dùng.
        - KHÔNG giải thích, KHÔNG thêm nội dung và giữa nguyên ý query.
        - Không trả về câu hỏi.
        - Trả về MỘT câu NGẮN GỌN nhất có thể (output)
        
        VÍ DỤ:

        Input:
        Tôi muốn ly hôn.  câu hỏi gợi ý: Bạn muốn ly hôn thuận tình hay đơn phương? câu trả lời của người dùng: ly hôn đơn phương, câu hỏi gợi ý: ....

        Output:
        Tôi muốn ly hôn đơn phương ?

        INPUT:
        {query}

        OUTPUT:
        """
    return llm.invoke(prompt).strip()