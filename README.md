# Pipeline RAG đa giai đoạn cho bài toán hỏi đáp văn bản pháp luật, tập trung vào tối ưu **recall** và **precision**

## 📌 Giới thiệu
Dự án xây dựng hệ thống **Retrieval-Augmented Generation (RAG)** nhằm nâng cao độ chính xác trong bài toán hỏi đáp, đặc biệt trong miền **văn bản pháp luật** – nơi có mối liên kết ngữ cảnh phức tạp giữa các điều khoản.

---

## ⚙️ Thành phần hệ thống
- **Query Rewriting (LLM)** → Chuẩn hóa truy vấn  
- **Semantic Cache** → Tăng tốc phản hồi  
- **Hybrid Retrieval (BM25 + Embedding)** → Tăng *recall*  
- **Reranking (Cross-Encoder)** → Tăng *precision*  
- **Context Validation Loop** → Đảm bảo đủ ngữ cảnh  

---

## 🔹 Tổng quan kiến trúc
```
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
```

---

## 🔹 1. Query Rewriting
### 🎯 Mục tiêu
Chuẩn hóa câu hỏi người dùng để tối ưu quá trình truy xuất.

### ⚙️ Phương pháp
```
q → q'
```

### ✅ Lợi ích
- Tăng khả năng match của **BM25**  
- Giảm ambiguity (mơ hồ ngữ nghĩa)  
- Chuẩn hóa câu hỏi rõ ràng hơn  

---

## 🔹 2. Semantic Cache
### ⚙️ Cơ chế hoạt động
Hệ thống lưu:
- Query trước đó: `q_i`  
- Embedding: `e_i`  
- Answer: `a_i`  

Khi có query mới:
```
e = Encoder(q')
sim(e, e_i) = cosine(e, e_i)
```

### 🎯 Quyết định
- Nếu:
```
max(sim) ≥ τ
```
→ **Cache Hit** → trả lời ngay  

- Ngược lại → **Cache Miss** → chuyển sang RAG  

### ✅ Lợi ích
- Giảm latency  
- Giảm chi phí LLM  
- Tái sử dụng tri thức  

---

## 🔹 3. Hybrid Retrieval
### ⚙️ Thành phần

**BM25 (Sparse Retrieval)**
- Dựa trên từ khóa  
- Hiệu quả với văn bản pháp luật  

**Embedding Search (Bi-Encoder)**
- Dựa trên vector ngữ nghĩa  
- Bắt semantic similarity  

### 📌 Kết quả
```
Candidates = {d1, d2, ..., dn}
```

---

## 🔹 4. Reranking (Cross-Encoder)
### ⚙️ Cách hoạt động
```
Input: [CLS] query [SEP] document [SEP]
```

### 📌 Kết quả
```
score_i = f(q', d_i)
```
→ Chọn **Top-K chunk quan trọng nhất**

---

## 🔹 5. Context Expansion (Pháp luật)
### 🎯 Vấn đề
- Các điều luật có liên kết với nhau  

### ⚙️ Giải pháp
- Trích xuất các điều liên quan từ Top-K  
- Mở rộng context  

### ✅ Lợi ích
- Tăng độ đầy đủ ngữ cảnh  
- Giảm sai sót  

---

## 🔹 6. Context Validation Loop
### ⚙️ Cơ chế
LLM kiểm tra:
> Context đã đủ để trả lời chưa?

### 🔁 Nếu chưa đủ
→ Hỏi lại người dùng (clarification)

### ⚠️ Giới hạn
- Tối đa **3 lượt hỏi**  
- Tránh loop vô hạn  

---

## 🔹 7. Answer Generation
```
(q', Context) → LLM → Answer
```

→ Sinh câu trả lời cuối cùng

---

## 🔹 So sánh Bi-Encoder vs Cross-Encoder

### 🔸 Bi-Encoder (Search Embedding)
```
q_vec = Encoder(query)
d_vec = Encoder(document)
score = cosine_similarity(q_vec, d_vec)
```

#### ✅ Ưu điểm
- Nhanh  
- Pre-compute được  
- Scale tốt  

#### ❌ Hạn chế
- Không có tương tác trực tiếp  
- Dễ sai ngữ cảnh  

---

### 🔸 Cross-Encoder (Reranker)
```
Input: [CLS] query [SEP] document [SEP]
score = Transformer(query ⊕ document)
```

#### ✅ Ưu điểm
- Hiểu tương tác token-level  
- Độ chính xác cao  

#### ❌ Hạn chế
- Chậm  
- Không scale tốt  

---

## 🔴 Vì sao Cross-Encoder chính xác hơn?
- **Attention toàn cục** → Query ↔ Document tương tác trực tiếp  
- **Hiểu ngữ nghĩa sâu** → Synonym, context, logic  
- **Tối ưu trực tiếp cho ranking**:
```
(query, document, relevance)
```

---

## 🔹 Kết hợp hiệu quả
```
Bi-Encoder   → Recall cao (lọc nhanh)
Cross-Encoder → Precision cao (xếp hạng lại)
```

---

## 🔹 Pipeline chi tiết
```
                 ┌────────────────────┐
                 │   User Question    │
                 └─────────┬──────────┘
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
     Answer                  Hybrid Retrieval
                                     ▼
                              Candidate Chunks
                                     ▼
                                Reranker
                                     ▼
                                  Top-K
                                     ▼
                           Context Expansion
                                     ▼
                           Context Validation
                                     │
                ┌────────────────────┴─────────────┐
                │                                  │
         Not Enough                         Enough Context
                │                                  │
                ▼                                  ▼
         Ask User (≤3)                    Answer Generation
                │                                  │
                └───────────────loop───────────────┘
                                               ▼
                                          Final Answer
```

---

## 🔹 Kết luận
Hệ thống đạt được sự cân bằng giữa:

- ⚡ **Efficiency (tốc độ)**  
- 🎯 **Effectiveness (độ chính xác)**  

Thông qua:
- Semantic Cache → giảm latency  
- Hybrid Retrieval → tăng recall  
- Cross-Encoder → tăng precision  
- Validation Loop → đảm bảo đủ ngữ cảnh  
