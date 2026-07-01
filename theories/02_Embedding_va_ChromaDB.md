# Vector Embedding & ChromaDB

## 1. Vector Embedding (Biểu diễn Vector) là gì?
- **Định nghĩa:** Là kỹ thuật ánh xạ các thực thể rời rạc (như từ ngữ, câu, đoạn văn) thành các điểm trong không gian vector liên tục n-chiều. Trong đồ án này, các câu/đoạn văn bản được biến đổi thành các vector 768 chiều (thông qua mô hình `gemini-embedding-2`).
- **Giả thuyết phân phối (Distributional Hypothesis):** Lý thuyết cơ bản đằng sau embedding là "ngôn ngữ học phân phối", phát biểu rằng "bạn sẽ biết nghĩa của một từ thông qua những từ đi cùng với nó". Mô hình AI học cách biểu diễn vector thông qua việc quan sát bối cảnh xuất hiện của từ/câu trong khối lượng lớn văn bản.
- **Biểu diễn ngữ nghĩa (Semantic Representation):** Thay vì biểu diễn bằng Sparse Vector (như One-hot encoding hay TF-IDF) nơi các chiều hoàn toàn độc lập, Dense Vector (Embedding) nén ý nghĩa ngôn ngữ vào không gian liên tục. Nhờ đó, tính chất hình học phản ánh tính chất ngữ nghĩa. Ví dụ: Từ "Học phí" và "Tiền học" sẽ có tọa độ rất gần nhau trong không gian vector dù mặt chữ khác nhau hoàn toàn.

### 1.1. Ý nghĩa của "Không gian 768 chiều"
- **Chiều (Dimension) là gì?** Trong không gian 2D, ta có thể đánh giá vật thể qua 2 tiêu chí (VD: Chiều X = Kích thước, Chiều Y = Độ nguy hiểm). Tọa độ [3, 4] sẽ đại diện cho một con vật nhỏ nhưng hơi dữ.
- Ngôn ngữ phức tạp hơn nhiều với vô vàn sắc thái (giới tính, thời gian, mức độ lịch sự, chuyên ngành...). Do đó, các mô hình AI như `gemini-embedding-2` được huấn luyện để phân tích văn bản thành **768 tiêu chí đánh giá** khác nhau.
- Mỗi câu nói sẽ biến thành một mảng chính xác gồm 768 con số (VD: `[0.012, -0.453, ..., 0.887]`). Đây chính là tọa độ định vị vị trí ngữ nghĩa của câu đó trong "bộ não" của AI.
- **Latent Dimensions (Các chiều ẩn):** Điểm đặc biệt về lý thuyết là các chiều này do máy tự học và tự gán (Latent). Con người không thể định nghĩa cụ thể chiều thứ 15 là "thời gian" hay chiều thứ 100 là "tiền bạc", nhưng mô hình biết cách phân phối ý nghĩa qua các chiều này để nhóm các câu tương đồng lại với nhau.

## 2. ChromaDB và Lưu trữ Vector (Vector Database)
- **Định nghĩa:** Là một cơ sở dữ liệu vector mã nguồn mở (Open-source Vector Database), được tối ưu hóa để lưu trữ và truy vấn các dense vectors ở quy mô lớn.
- **Kiến trúc cục bộ (Local-first):** Khác với Pinecone hay Weaviate hoạt động trên cloud, ChromaDB được thiết kế để nhúng trực tiếp (embedded) vào ứng dụng, chạy cục bộ trên RAM và ổ cứng. Điều này mang lại độ trễ truy xuất cực thấp (latency ~14ms) và đảm bảo tính bảo mật dữ liệu toàn vẹn do không cần gọi qua mạng Internet.
- **Cơ chế lưu trữ:** Lưu trữ đồng thời Document (văn bản gốc), Metadata (thông tin đi kèm như nguồn, tác giả, số trang) và Vector Embeddings, giúp việc truy xuất tài liệu kèm ngữ cảnh thuận tiện.

## 3. Lý thuyết Tìm kiếm tương đồng (Similarity Search)
Khi người dùng đặt câu hỏi, hệ thống sẽ thực hiện các bước sau:
1. Chuyển đổi câu hỏi thành Query Vector (cùng không gian 768 chiều).
2. Thực hiện so khớp Query Vector với toàn bộ Knowledge Vectors trong CSDL.
3. Các độ đo khoảng cách (Distance Metrics) phổ biến:
   - **Tích vô hướng (Dot Product):** Nhân các thành phần tương ứng của hai vector và cộng lại. Điểm càng cao thì càng giống nhau.
   - **Cosine Similarity (Độ tương đồng Cosine):** Đo góc giữa 2 vector trong không gian. Góc càng nhỏ (Cosine tiến tới 1), hai văn bản càng có ngữ nghĩa tương đồng, bất kể độ dài văn bản khác nhau.
   - **L2 Distance (Khoảng cách Euclidean):** Đo khoảng cách đường thẳng giữa 2 điểm vector.
ChromaDB tính toán nhanh các độ đo này để trả về Top K tài liệu có độ liên quan cao nhất.

## 4. Thuật toán HNSW (Hierarchical Navigable Small World) trong ChromaDB
- Để tìm kiếm trong một tập dữ liệu khổng lồ, việc tính toán tuần tự với từng vector (Exhaustive KNN - K-Nearest Neighbors) là bất khả thi về mặt hiệu năng (độ phức tạp O(N)).
- ChromaDB giải quyết bài toán này bằng **HNSW**, một thuật toán tìm kiếm hàng xóm gần nhất xấp xỉ (Approximate Nearest Neighbor - ANN).
- **Nguyên lý HNSW:** Thuật toán xây dựng một đồ thị mạng lưới phân cấp nhiều tầng. Tầng trên cùng có ít điểm (node) nối với nhau bằng các liên kết dài, giúp "bước nhảy xa" để nhanh chóng khoanh vùng không gian chứa vector. Càng xuống các tầng dưới, số node càng dày đặc và liên kết ngắn lại, cho phép tinh chỉnh vị trí để tìm ra chính xác các vector gần nhất. Nhờ HNSW, tốc độ truy vấn giảm xuống còn O(log N).

## 5. Chunking (Phân mảnh dữ liệu) trước khi Embedding
- **Giới hạn Context Window:** Các mô hình nhúng (Embedding Models) luôn có giới hạn độ dài đầu vào tối đa (ví dụ: 2048 hoặc 8192 token).
- Việc chia nhỏ văn bản dài thành các đoạn (chunks) có kích thước phù hợp không chỉ để đáp ứng đầu vào của mô hình, mà còn để tăng độ chính xác cho việc tìm kiếm. Nếu chunk quá lớn, vector sẽ bị "loãng" ngữ nghĩa (chứa quá nhiều ý khác nhau); nếu chunk quá nhỏ, đoạn văn mất đi bối cảnh (context).
- Kỹ thuật **Chunk Overlap** (chồng lấn văn bản giữa các đoạn) thường được dùng để duy trì tính liền mạch về mặt ngữ nghĩa, tránh việc chia cắt câu ở đoạn giữa những ý quan trọng.

## 6. Semantic Cache (Bộ nhớ đệm ngữ nghĩa) trong dự án
- **Có sử dụng không?** Có. Dự án có tích hợp hệ thống Semantic Cache.
- **Nó được triển khai ở đâu?** Logic cốt lõi nằm ở file `codebase/src/core/semantic_cache.py` và được tích hợp trực tiếp vào luồng xử lý chat ở `codebase/src/core/chat_service.py`.
- **Cơ chế hoạt động thực tế trong dự án:**
  - **Công nghệ lưu trữ:** Sử dụng SQLite để lưu trữ các cache với file database cục bộ (`semantic_cache.db`).
  - **Ngưỡng tương đồng (Similarity Threshold):** Hệ thống cài đặt ngưỡng tương đồng ngữ nghĩa rất cao: `0.96`.
  - **Quá trình đánh chặn (Intercept):**
    1. Khi người dùng đặt câu hỏi, câu hỏi ngay lập tức được biến đổi thành vector (Embedding).
    2. Hệ thống tìm kiếm vector này trong DB Cache SQLite.
    3. Nếu phát hiện có câu hỏi cũ với độ tương đồng vector $\ge 0.96$ (*Cache Hit*), hệ thống sẽ trả ngay câu trả lời đã lưu trước đó. Điều này giúp giảm thời gian phản hồi từ vài giây xuống chỉ vài mili-giây và tiết kiệm chi phí gọi LLM.
    4. Nếu không tìm thấy (*Cache Miss*), hệ thống mới thực hiện luồng RAG thông thường (tìm kiếm trong ChromaDB $\rightarrow$ gọi LLM tạo câu trả lời). Sau khi có kết quả, cặp Câu hỏi - Trả lời mới sẽ được tự động lưu ngược lại vào Cache.
  - **Quản lý bộ nhớ:** Để tránh đầy ổ cứng, Cache giới hạn lưu trữ tối đa 1000 bản ghi (`CACHE_MAX_ROWS = 1000`) và mỗi bản ghi chỉ tồn tại tối đa 30 ngày (`CACHE_TTL_SECONDS = 30 * 24 * 3600`). Đồng thời khi dữ liệu gốc thay đổi, VectorDB cũng kích hoạt hàm `_invalidate_cache()` để xóa cache cũ, đảm bảo tính cập nhật.
