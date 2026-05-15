def rewrite_query_llm(query, llm,first=True):
    if first:
        prompt=f"""
        Chuẩn hóa câu hỏi Tiếng Việt về luật hôn nhân & gia đình (sửa chính tả, ngữ pháp, làm rõ nghĩa).
        Yêu cầu: Giữ nguyên ý nghĩa, KHÔNG để dấu kết thúc câu, CHỈ trả về duy nhất câu NGẮN GỌN nhất, không giải thích.
          Câu hỏi: {query}

        """
    else:
        prompt = f"""
        Bạn là hệ thống chuẩn hóa câu hỏi pháp luật Hôn nhân và Gia đình.

        NHIỆM VỤ:
        - Từ hội thoại gồm: câu hỏi ban đầu + câu hỏi gợi ý + câu trả lời của người dùng cho câu hỏi gợi ý.
        - Hãy suy luận ra câu đầy đủ nhu cầu của người dùng (query).

        QUY TẮC BẮT BUỘC:
        - Suy luận vè viết lại câu hỏi từ ngữ cảnh câu hỏi ban đầu, kết hợp thông tin từ câu hỏi gợi ý và câu trả lời của người dùng.
        - KHÔNG giải thích, KHÔNG thêm nội dung và giữa nguyên ý query.
        - Chỉ trả về MỘT câu NGẮN GỌN nhất (output).
        - Tiếng Việt.

        VÍ DỤ:

        Input:
        Tôi muốn ly hôn.  câu hỏi gợi ý: Bạn muốn ly hôn thuận tình hay đơn phương? câu trả lời của người dùng: ly hôn đơn phương.

        Output:
        Tôi muốn ly hôn đơn phương

        INPUT:
        {query}

        OUTPUT:
        """
    return llm.invoke(prompt).strip()
