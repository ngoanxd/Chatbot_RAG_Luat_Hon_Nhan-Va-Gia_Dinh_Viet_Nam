# LegalRAG Pipeline  
### Pipeline RAG cho hỏi đáp pháp luật với hybrid retrieval và cross-encoder reranking

> Pipeline Retrieval-Augmented Generation đa giai đoạn cho bài toán hỏi đáp văn bản pháp luật, tối ưu hóa **recall** trong truy xuất và **precision** trong tái xếp hạng.

---

## 1. Problem Statement
Bài toán hỏi đáp trong miền văn bản pháp luật gặp nhiều thách thức:

- Ngôn ngữ mang tính hình thức và phức tạp  
- Các điều khoản có liên kết chéo (cross-reference)  
- Truy vấn người dùng thường mơ hồ hoặc thiếu ngữ cảnh  

Mục tiêu của dự án là xây dựng một pipeline RAG nhằm:
- Truy xuất chính xác các điều luật liên quan  
- Đảm bảo đầy đủ ngữ cảnh  
- Sinh câu trả lời có độ tin cậy cao  

---

## 2. Approach Overview

```
<img width="1774" height="887" alt="image" src="https://github.com/user-attachments/assets/f3f89897-a516-44f6-901b-67e2b6350ebf" />

```

---

## 3. Key Components

### 3.1 Query Rewriting
Chuẩn hóa truy vấn đầu vào bằng mô hình ngôn ngữ:

```
q → q'
```

Giúp giảm ambiguity và cải thiện khả năng truy xuất.

---

### 3.2 Semantic Cache
Lưu trữ các bộ:

- Query: `q_i`  
- Embedding: `e_i`  
- Answer: `a_i`  

Với truy vấn mới:

```
e = Encoder(q')
sim(e, e_i) = cosine(e, e_i)
```

Nếu `max(sim) ≥ τ` → trả lời trực tiếp.

---

### 3.3 Hybrid Retrieval

Kết hợp hai phương pháp:

| Phương pháp   | Vai trò |
|--------------|--------|
| BM25         | Keyword matching |
| Bi-Encoder   | Semantic matching |

Mục tiêu: tăng khả năng bao phủ (recall).

---

### 3.4 Cross-Encoder Reranking

```
Input: [CLS] query [SEP] document [SEP]
score = Transformer(query ⊕ document)
```

Đánh giá lại độ liên quan và chọn Top-K kết quả tốt nhất.

---

### 3.5 Context Expansion
Mở rộng ngữ cảnh dựa trên các điều luật liên quan nhằm xử lý tính liên kết trong văn bản pháp luật.

---

### 3.6 Context Validation
Mô hình đánh giá mức độ đầy đủ của context. Nếu chưa đủ, hệ thống yêu cầu bổ sung thông tin (tối đa 3 lượt).

---

### 3.7 Answer Generation

```
(q', context) → LLM → answer
```

Sinh câu trả lời cuối cùng dựa trên ngữ cảnh đã được xác thực.

---

## 4. Bi-Encoder vs Cross-Encoder

| Tiêu chí        | Bi-Encoder | Cross-Encoder |
|----------------|-----------|--------------|
| Tốc độ         | Nhanh     | Chậm |
| Khả năng scale | Tốt       | Hạn chế |
| Độ chính xác   | Trung bình | Cao |
| Tương tác      | Không     | Có |

Nhận xét:
- Bi-Encoder phù hợp cho retrieval (tối ưu recall)  
- Cross-Encoder phù hợp cho reranking (tối ưu precision)  

---

## 5. Evaluation (Suggested)

Các metric đề xuất:

- Recall@K  
- Mean Reciprocal Rank (MRR)  
- Latency  

---

## 6. Experiment Setup

- Corpus: Văn bản pháp luật  
- Chunking: theo điều/khoản  
- Retrieval: BM25 + Sentence Embedding  
- Reranking: Cross-Encoder  

---

## 7. Performance Insights

- Hybrid retrieval cải thiện recall đáng kể  
- Reranking cải thiện precision rõ rệt  
- Semantic cache giúp giảm latency  

---

## 8. Project Structure

```
.
.
├── data/
│   └── loader.py                 # Load dữ liệu (PDF, txt luật)
│
├── retriever/                   # Truy xuất (BM25, FAISS)
│   ├── bm25.py
│   ├── faiss_db.py
│   └── hybrid_search.py
│
├── luat_hon_nhan/               # Dữ liệu luật
│
├── cache/                       # Semantic cache
│   ├── cache_semantic.py
│   └── cache_semantic.json
│
├── llm/                         # Xử lý LLM
│   ├── analyze.py
│   ├── model.py
│   └── rewrite.py
│
├── faiss_store/                 # Vector DB
│   ├── index.faiss
│   └── index.pkl
│
├── utils/                       # Helper functions
│   └── json_utils.py
│
├── build_index.py               # Script build vector DB
├── requirements.txt 
│
├── config.py                    # Cấu hình hệ thống
│
└── main.py                      # Entry point chính
```

---

## 9. How to Run

```bash
git clone <repo>
cd project
pip install -r requirements.txt
python main.py

All in:(guide_run.ipynb) google colab 
```

---

## 10. Conclusion

Pipeline đạt được sự cân bằng giữa:

- Efficiency (tốc độ)  
- Effectiveness (độ chính xác)  

Thông qua việc kết hợp:
- Hybrid retrieval  
- Cross-encoder reranking  
- Semantic caching  
- Context validation  

Phù hợp cho bài toán hỏi đáp trong miền pháp luật.

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/2e5e0b9e-33d3-4f9e-8faf-cb441624fd05" />




---
