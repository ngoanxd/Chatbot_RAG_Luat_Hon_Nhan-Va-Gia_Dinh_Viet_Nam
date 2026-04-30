

🔹 RAG Pipeline with Semantic Cache & Query Rewriting
📌 Giới thiệu

Dự án xây dựng hệ thống Retrieval-Augmented Generation (RAG) nhằm nâng cao độ chính xác trong bài toán hỏi đáp, đặc biệt trong miền văn bản pháp luật – nơi có tính liên kết ngữ cảnh cao giữa các điều khoản.

Hệ thống kết hợp nhiều thành phần:

Query Rewriting (LLM) → chuẩn hóa truy vấn
Semantic Cache → tăng tốc phản hồi
Hybrid Retrieval (BM25 + Embedding) → tăng recall
Reranking (Cross-Encoder) → tăng precision
Context Validation Loop → đảm bảo đủ ngữ cảnh trước khi trả lời
🔹 Tổng quan kiến trúc
User Query 
   ↓
Query Rewriting (LLM)
   ↓
Semantic Cache (Hit → trả lời | Miss → RAG)
   ↓
Hybrid Retrieval (BM25 + Embedding)
   ↓
Reranker (Cross-Encoder)
   ↓
Context Expansion (Legal Linking)
   ↓
Context Validation (LLM)
   ↓
Answer Generation (LLM)
🔹 1. Query Rewriting
Mục tiêu

Chuẩn hóa câu hỏi người dùng nhằm tối ưu cho quá trình truy xuất.

Phương pháp

Sử dụng LLM để biến đổi:

q→q
′
Lợi ích
Tăng khả năng match của BM25
Giảm ambiguity (mơ hồ ngữ nghĩa)
Chuẩn hóa câu hỏi về dạng rõ ràng hơn
🔹 2. Semantic Cache
Cơ chế

Hệ thống lưu:

Query trước đó q
i
	​

Embedding e
i
	​

Answer a
i
	​


Khi có query mới:

e=Encoder(q
′
)

So sánh:

sim(e,e
i
	​

)=cosine(e,e
i
	​

)
Quyết định
Nếu:
max(sim)≥τ

→ Cache Hit → trả lời ngay

Ngược lại:
→ Cache Miss → chuyển sang RAG
Lợi ích
Giảm latency
Giảm chi phí LLM
Tái sử dụng tri thức đã có
🔹 3. Hybrid Retrieval
Thành phần
BM25 (Sparse Retrieval)
Dựa trên từ khóa
Hiệu quả với văn bản pháp luật
Embedding Search (Bi-Encoder)
Dựa trên vector ngữ nghĩa
Bắt được semantic similarity
Kết quả
Candidates={d
1
	​

,d
2
	​

,...,d
n
	​

}
🔹 4. Reranking (Cross-Encoder)

Các candidate được đánh giá lại bằng mô hình cross-encoder:

Input: [CLS] query [SEP] document [SEP]

Ví dụ mô hình: BAAI/bge-reranker-v2-m3

Kết quả
score
i
	​

=f(q
′
,d
i
	​

)

→ Chọn Top-K chunk quan trọng nhất

🔹 5. Context Expansion (Pháp luật)

Do văn bản luật có tính liên kết:

Một điều khoản thường liên quan điều khác
→ Hệ thống mở rộng context bằng cách:
Trích xuất các điều liên quan từ Top-K
Kết hợp thành context hoàn chỉnh
🔹 6. Context Validation Loop

LLM đánh giá:

Context đã đủ để trả lời chưa?
Nếu chưa đủ

→ Sinh câu hỏi làm rõ (clarification)

Giới hạn
Tối đa 3 lượt hỏi
→ Tránh vòng lặp vô hạn
🔹 7. Answer Generation

Khi đủ ngữ cảnh:

(q
′
,Context)→LLM→Answer

→ Sinh câu trả lời cuối cùng

🔹 So sánh Bi-Encoder vs Cross-Encoder
Bi-Encoder (Search Embedding)
q_vec = Encoder(query)
d_vec = Encoder(document)
score = cosine_similarity(q_vec, d_vec)
Ưu điểm
Tốc độ nhanh
Có thể pre-compute
Phù hợp retrieval lớn
Hạn chế
Không có tương tác trực tiếp giữa query và document
Dễ sai ngữ cảnh
Cross-Encoder (Reranker)
Input: [CLS] query [SEP] document [SEP]
score = Transformer(query ⊕ document)
Ưu điểm
Hiểu tương tác token-level
Độ chính xác cao
Hạn chế
Chậm
Không scale tốt
🔴 Vì sao Cross-Encoder chính xác hơn?
1. Attention toàn cục
Token query ↔ token document tương tác trực tiếp
2. Hiểu ngữ nghĩa sâu
Nhận diện synonym, context, logic
3. Học trực tiếp bài toán ranking
Training trên (query, doc, relevance)
🔹 Kết hợp hiệu quả
Bi-Encoder → Recall cao (lọc nhanh)
Cross-Encoder → Precision cao (xếp hạng lại)
🔹 Sơ đồ chi tiết toàn pipeline
                 ┌────────────────────┐
                 │   User Question    │
                 └─────────┬──────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Query Rewriting    │
                └─────────┬──────────┘
                           ▼
                ┌────────────────────┐
                │ Semantic Cache     │
                └───────┬────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
   Cache Hit                       Cache Miss
        │                               │
        ▼                               ▼
  ┌────────────┐           ┌────────────────────────┐
  │  Answer    │           │ Hybrid Retrieval       │
  └────────────┘           └─────────┬──────────────┘
                                     ▼
                          ┌────────────────────┐
                          │ Candidate Chunks   │
                          └─────────┬──────────┘
                                    ▼
                          ┌────────────────────┐
                          │ Reranker           │
                          └─────────┬──────────┘
                                    ▼
                          ┌────────────────────┐
                          │ Top-K              │
                          └─────────┬──────────┘
                                    ▼
                          ┌────────────────────┐
                          │ Context Expansion  │
                          └─────────┬──────────┘
                                    ▼
                          ┌────────────────────┐
                          │ Context Validation │
                          └───────┬────────────┘
                                  │
                 ┌────────────────┴──────────────┐
                 │                               │
           Not Enough                    Enough Context
                 │                               │
                 ▼                               ▼
       Ask User (≤3 turns)          Answer Generation
                 │                               │
                 └────────────loop───────────────┘
                                                 ▼
                                          Final Answer
🔹 Kết luận

Hệ thống kết hợp:

Semantic Cache → tối ưu hiệu năng
Hybrid Retrieval → tăng recall
Cross-Encoder → tăng precision
Validation Loop → đảm bảo tính đầy đủ ngữ cảnh

→ Tạo ra một pipeline cân bằng giữa:

Efficiency (tốc độ)
Effectiveness (độ chính xác)
