📌 Giới thiệu

    Dự án xây dựng hệ thống Retrieval-Augmented Generation (RAG) – một kiến trúc kết hợp giữa truy xuất thông tin (retrieval) và mô hình ngôn ngữ lớn (LLM) nhằm nâng cao độ chính xác và tính ngữ cảnh trong quá trình sinh câu trả lời.
    
    <img width="377" height="356" alt="image" src="https://github.com/user-attachments/assets/00477e44-e51a-4ec6-8827-cfda779378a8" />
                                    RAG Pipeline

Trong hệ thống này, các văn bản pháp luật liên quan đến Luật Hôn nhân và Gia đình Việt Nam được truy xuất theo ngữ nghĩa, sau đó được xử lý và tổng hợp bởi mô hình ngôn ngữ để tạo ra câu trả lời tự nhiên, có căn cứ và dễ hiểu.

⚙️ Kiến trúc hệ thống

   Hệ thống được xây dựng dựa trên các thành phần chính:

Embedding Model: BAAI/bge-m3
Biểu diễn văn bản dưới dạng vector ngữ nghĩa phục vụ truy xuất thông tin.
Reranker Model: BAAI/bge-reranker-v2-m3
Tái xếp hạng các đoạn văn bản được truy xuất nhằm tăng độ chính xác và mức độ liên quan.
Large Language Model (LLM): Qwen3
Sinh câu trả lời cuối cùng dựa trên ngữ cảnh đã được chọn lọc.
