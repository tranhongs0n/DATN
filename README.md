# 🤖 Gemini Multimodal RAG - Tuyển sinh TLU

Hệ thống RAG đa phương thức hỗ trợ tra cứu thông tin tuyển sinh Đại học Thủy Lợi sử dụng Gemini 2.0 Flash.

## 📁 Cấu trúc dự án
- `src/app`: Chứa giao diện Gradio.
- `src/core`: Các engine RAG chính (Multimodal & Vector DB).
- `src/utils`: Các công cụ hỗ trợ (Scraper, Loader).
- `src/config`: Cấu hình hệ thống.
- `data/`: Chứa các tài liệu tuyển sinh (PDF, DOCX, Ảnh).

## 🚀 Hướng dẫn sử dụng

### 1. Cài đặt môi trường
```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

### 2. Cấu hình
Tạo file `.env` từ `.env.example` và thêm `GOOGLE_API_KEY`.

### 3. Chạy ứng dụng
Sử dụng CLI thống nhất:

- **Khởi chạy Giao diện (Mặc định):**
  ```bash
  python main.py ui
  ```

- **Thu thập dữ liệu từ Website:**
  ```bash
  python main.py scrape --limit 5
  ```

- **Xây dựng Vector Database:**
  ```bash
  python main.py build-db
  ```

## 🛠️ Công nghệ sử dụng
- **Google Gen AI SDK** (Bản mới nhất cho Gemini 3)
- Gemini 3 Flash (Multimodal)
- LangChain & ChromaDB
- Gradio UI
- BeautifulSoup4 (Scraping)
