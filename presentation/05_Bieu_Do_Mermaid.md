# TỔNG HỢP CÁC BIỂU ĐỒ UML SẴN SÀNG ĐỂ COPY

Bạn có thể copy các khối code dưới đây và dán vào [https://mermaid.live/](https://mermaid.live/) để xuất ra file ảnh (PNG/SVG) chất lượng cao và dán vào Slide hoặc Báo cáo.

## 1. Sơ đồ Use Case Tổng Quát
```mermaid
flowchart LR
    ThíSinh(("👤 Thí Sinh/Phụ huynh"))
    Admin(("👨‍💼 Ban Tuyển Sinh"))
    
    subgraph Hệ thống Trợ lý ảo RAG
        UC1([Nhắn tin tra cứu qua Zalo Bot])
        UC2([Đăng nhập Hệ thống Admin])
        UC3([Quản lý kho Quy chế Tuyển sinh])
        UC4([Quản lý Từ điển Viết tắt])
        UC5([Xem lại Lịch sử hội thoại])
        UC6([Cào dữ liệu web tự động])
    end
    
    ThíSinh --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
```

## 2. Biểu đồ Hoạt động (Activity Diagram) - Luồng Chatbot
```mermaid
flowchart TD
    Start([Bắt đầu]) --> Nhận[Nhận câu hỏi từ Zalo]
    Nhận --> Filter[Tiền xử lý: Dịch từ viết tắt qua SQLite]
    Filter --> Rule{Intent hợp lệ?}
    
    Rule -- Sai (Câu hỏi ngoài luồng) --> Reject[Từ chối trả lời] --> B[Gửi tin nhắn về Zalo] --> End([Kết thúc])
    
    Rule -- Đúng --> Embed[Mã hóa Vector câu hỏi (Gemini Embedding)]
    Embed --> Cache{Kiểm tra Semantic Cache
Độ tương đồng > 95%?}
    
    Cache -- Có (Trúng đệm) --> Hit[Lấy câu trả lời sẵn từ Cache] --> B
    
    Cache -- Không (Trượt đệm) --> DB[Tìm Top 5 Context trong ChromaDB]
    DB --> LLM[Gửi Context + Câu hỏi cho Gemini LLM]
    LLM --> Sinh[Gemini sinh câu trả lời]
    Sinh --> Save[Lưu kết quả vào Cache & SQLite ChatLogs]
    Save --> B
```

## 3. Biểu đồ Tuần tự (Sequence Diagram) - RAG Streaming
```mermaid
sequenceDiagram
    autonumber
    actor ThíSinh as Thí Sinh (Zalo App)
    participant Zalo as Zalo Server
    participant FastAPI as Backend (FastAPI)
    participant SQLite as CSDL (SQLite)
    participant ChromaDB as Vector DB
    participant Gemini as Google Gemini API

    ThíSinh->>Zalo: Gửi tin nhắn ("điểm chuẩn cntt")
    Zalo->>FastAPI: Forward Request (Webhook JSON)
    FastAPI->>SQLite: Query Từ viết tắt
    SQLite-->>FastAPI: Trả về ("cntt" -> "Công nghệ thông tin")
    
    FastAPI->>Gemini: Gọi Embedding API ("điểm chuẩn Công nghệ thông tin")
    Gemini-->>FastAPI: Trả về Vector 768 chiều
    
    FastAPI->>ChromaDB: Tìm kiếm ngữ nghĩa (Vector, top_k=5)
    ChromaDB-->>FastAPI: Trả về 5 đoạn văn bản quy chế
    
    FastAPI->>Gemini: Gọi LLM (System Prompt + Context + Câu hỏi)
    Gemini-->>FastAPI: Trả về Câu trả lời
    
    FastAPI->>Zalo: Bắn API Gửi tin nhắn 
    Zalo-->>ThíSinh: Hiển thị câu trả lời trên điện thoại
    FastAPI->>SQLite: Lưu Audit Log & Chat Log (Async)
```

## 4. Mô hình Cơ sở dữ liệu (ERD)
```mermaid
erDiagram
    USERS {
        int id PK
        string username
        string hashed_password
        string role
        datetime created_at
    }
    DOCUMENTS {
        int id PK
        string file_name
        string status "Uploaded, Embedded"
        datetime upload_time
    }
    DICTIONARIES {
        int id PK
        string short_word
        string full_word
    }
    CHAT_LOGS {
        int id PK
        string zalo_id
        string question
        string answer
        float latency_ms
        boolean is_cached
        datetime created_at
    }
    
    USERS ||--o{ DOCUMENTS : "quản lý"
    USERS ||--o{ DICTIONARIES : "cập nhật"
```
