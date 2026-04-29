📌 Giới thiệu

Dự án được xây dựng dựa trên kiến trúc Retrieval-Augmented Generation (RAG) – một phương pháp kết hợp giữa cơ chế truy xuất thông tin (information retrieval) và mô hình ngôn ngữ lớn (Large Language Model – LLM). Kiến trúc này nhằm cải thiện độ chính xác, tính đầy đủ ngữ cảnh và khả năng giải thích của câu trả lời trong các hệ thống hỏi đáp tự động.

Trong hệ thống này, dữ liệu pháp luật thuộc Luật Hôn nhân và Gia đình Việt Nam được xử lý và truy xuất theo hướng ngữ nghĩa. Các đoạn văn bản liên quan sẽ được chọn lọc, sau đó đưa vào mô hình ngôn ngữ để sinh ra câu trả lời tự nhiên, có căn cứ pháp lý rõ ràng và dễ hiểu đối với người dùng.

⚙️ Kiến trúc hệ thống

Hệ thống được thiết kế dựa trên các thành phần chính sau:

🔹 Embedding Model

Sử dụng mô hình BAAI/bge-m3 để chuyển đổi văn bản thành các vector biểu diễn ngữ nghĩa trong không gian embedding. Các vector này được sử dụng làm cơ sở cho quá trình truy xuất thông tin theo độ tương đồng.

🔹 Reranker Model

Áp dụng mô hình BAAI/bge-reranker-v2-m3 nhằm tái xếp hạng các đoạn văn bản được truy xuất ban đầu. Giai đoạn này giúp nâng cao độ chính xác bằng cách đánh giá lại mức độ liên quan giữa truy vấn và các đoạn ứng viên.

🔹 Large Language Model (LLM)

Sử dụng mô hình Qwen3 chạy cục bộ (local inference) để tổng hợp thông tin và sinh câu trả lời cuối cùng dựa trên ngữ cảnh đã được chọn lọc từ bước truy xuất.

🧩 Xử lý dữ liệu

Dữ liệu pháp luật được tiền xử lý theo hướng chunking theo điều luật, trong đó mỗi điều trong bộ luật được tách thành một đơn vị dữ liệu độc lập (chunk). Cách tiếp cận này giúp đảm bảo khả năng truy xuất đầy đủ nội dung và tránh thiếu hụt ngữ cảnh.

Ví dụ, Luật Hôn nhân và Gia đình năm 2014 gồm 133 điều được tách thành 133 chunk. Tuy nhiên, do Điều 3 mang tính chất giải thích thuật ngữ nên đã được loại bỏ, dẫn đến tổng số còn 132 chunk.

Mỗi chunk được gắn metadata nhằm hỗ trợ truy vết và debug kết quả, ví dụ:

source: tên chương trong bộ luật
dieu: số điều tương ứng

Ví dụ:

metadata = {'source': 'cap_duong', 'dieu': 107}

Cách tổ chức này giúp hệ thống dễ dàng xác định vị trí pháp lý của thông tin cũng như cải thiện khả năng kiểm soát và giải thích kết quả truy vấn.

🔎 Chiến lược truy xuất (Retrieval)

Hệ thống sử dụng kết hợp ba phương pháp truy xuất nhằm tối ưu độ chính xác:

1. BM25

BM25 được sử dụng để khai thác mức độ trùng khớp từ khóa giữa truy vấn và tài liệu. Tuy nhiên, do đặc thù phương pháp dựa trên từ vựng, dữ liệu được tiền xử lý như sau:

Chuẩn hóa truy vấn bằng LLM để cải thiện ngữ nghĩa và hình thái câu
Chuyển toàn bộ văn bản về chữ thường (lower())
Token hóa bằng phương pháp split() theo khoảng trắng
2. Semantic Search (Embedding-based)

Sử dụng mô hình BAAI/bge-m3, hệ thống thực hiện truy xuất dựa trên độ tương đồng ngữ nghĩa giữa vector truy vấn và vector tài liệu. Do mô hình đã hỗ trợ đa ngôn ngữ và truy vấn đã được chuẩn hóa, nên không cần thực hiện tách từ tiếng Việt.

Qua thực nghiệm, phương pháp embedding cho kết quả chính xác và ổn định hơn BM25, do đó được ưu tiên với cấu hình:

k_faiss = 12
k_bm25 = 5
3. Reranking

Giai đoạn reranking sử dụng mô hình BAAI/bge-reranker-v2-m3, một mô hình cross-encoder đa ngôn ngữ. Kết quả thực nghiệm cho thấy mô hình này vượt trội so với các mô hình huấn luyện riêng cho tiếng Việt như PhoBERT hoặc các biến thể fine-tune như VoVanPhuSimBCE về độ chính xác xếp hạng.

🧠 Mô hình ngôn ngữ lớn (LLM)

Hệ thống sử dụng LLM chạy cục bộ nhằm giảm phụ thuộc vào API bên ngoài. Trong các mô hình thử nghiệm trên nền tảng Ollama, Qwen3 cho thấy sự cân bằng tốt giữa hiệu năng và tốc độ xử lý, đồng thời đảm bảo tính ổn định trong quá trình suy luận.
