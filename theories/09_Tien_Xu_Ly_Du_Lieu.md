# Tiền Xử Lý Dữ Liệu (Data Pre-processing) trong RAG

Giai đoạn tiền xử lý quyết định đến 80% độ chính xác của một hệ thống RAG (Retrieval-Augmented Generation). Trái với suy nghĩ thông thường là "cứ quăng file PDF vào cho AI tự đọc", dữ liệu thô thường chứa rất nhiều nhiễu, mất cấu trúc và từ lóng.

Dưới đây là 3 bước kỹ thuật chuyên sâu mà hệ thống đang sử dụng để làm sạch bộ nhớ tri thức trước khi nạp vào Vector Database (ChromaDB):

## 1. Chuyển đổi định dạng (PDF sang Markdown)
- **Vấn đề của PDF truyền thống:** Các thư viện đọc PDF cũ (như PyPDF2 hay PDFMiner) thường dùng kỹ thuật "cào chữ" (text extraction) bằng cách quét tọa độ (x,y) trên trang giấy. Điều này dẫn đến hậu quả nghiêm trọng: **Bảng biểu (Tables) bị vỡ nát** thành một dòng chữ dính liền nhau, và **Tiêu đề (Headings) bị mất cấu trúc**. Khi đó, RAG cắt đoạn (chunking) sẽ cắt bừa bãi khiến ý nghĩa bị phá vỡ.
- **Giải pháp của hệ thống:** Dự án áp dụng kỹ thuật Parsing cấu trúc cao (thông qua thư viện AI thị giác máy tính như `Docling` hoặc Gemini Vision).
- **Luồng xử lý (tại `codebase/src/core/indexing.py`):**
  1. Đọc file PDF nguyên bản.
  2. Bóc tách Layout (nhận diện đâu là tiêu đề, đâu là đoạn văn, đâu là bảng).
  3. Gọi hàm `export_to_markdown()`. 
  4. Hệ quả là bảng biểu được giữ nguyên dưới dạng `| Cột 1 | Cột 2 |`, các tiêu đề lớn biến thành `# Heading 1`. 
- **Lợi ích:** Markdown là ngôn ngữ "vàng" cho RAG. Việc giữ lại ký tự `#` và ngắt dòng `\n\n` giúp thuật toán `RecursiveCharacterTextSplitter` có điểm neo (anchor) để cắt tài liệu chuẩn xác 100% theo từng phần thay vì cắt ngẫu nhiên giữa chừng một bảng dữ liệu.

## 2. Làm sạch dữ liệu (Data Cleaning & Abbreviation)
Dữ liệu sinh viên nhập vào hoặc lấy từ Web thường không nhất quán.
- **Bi chuẩn hóa chuỗi (Normalization):** Chuyển đổi các bảng mã tiếng Việt bị lỗi (Unicode tổ hợp vs Unicode dựng sẵn) về một chuẩn duy nhất, xóa bỏ khoảng trắng thừa.
- **Xử lý Ngôn ngữ GenZ & Viết tắt (Abbreviation Resolution):**
  - **Vấn đề:** Trong cơ sở dữ liệu có ghi "Công nghệ thông tin". Thí sinh lại chat là "điểm chuẩn cntt là bnhiu". Thuật toán Embedding sẽ không nhận ra "cntt" là "Công nghệ thông tin" (điểm Cosine Similarity rất thấp).
  - **Giải pháp:** Hệ thống đã xây dựng một cơ sở dữ liệu nội bộ (Từ điển từ lóng) dành riêng cho lĩnh vực giáo dục. Trước khi câu hỏi được gửi đi Embedding, thuật toán sẽ tiền xử lý câu chữ: thay thế toàn bộ "cntt" -> "Công nghệ thông tin", "tl" -> "Thủy lợi", "kỹ thuật pm" -> "Kỹ thuật phần mềm".

## 3. Xóa mã rác và Tiêu âm (Removing Junk/Noise)
Không phải text nào cũng có giá trị nhúng vào CSDL. Việc mang "rác" đi nhúng vector (embedding) không những làm lãng phí tiền API mà còn tạo ra hiện tượng nhiễu sóng (Hallucination) cho AI.
- **Đối với tệp văn bản (PDF/Word):**
  - Hệ thống loại bỏ các đoạn Header/Footer (như tên trường Đại học Thủy Lợi xuất hiện ở đỉnh mỗi trang giấy).
  - Bỏ đi các Số trang (1, 2, 3...) chèn giữa các câu chữ.
  - Xóa bỏ các hình mờ (Watermarks).
- **Đối với dữ liệu Cào từ Web (Scraping):**
  - Khi thu thập bài báo tuyển sinh (tại `admin_scrape.py`), hệ thống dùng BeautifulSoup để cắt bỏ toàn bộ các thẻ `<script>`, `<style>`, `<footer>`, `<nav>` (menu điều hướng).
  - Chỉ trích xuất thẻ `<article>` hoặc `<main>` - nơi chứa 100% nội dung thuần của văn bản để đem đi Chunking. 

Nhờ 3 quy trình "Lọc máu" cực kỳ gắt gao này, các đoạn văn bản lưu trong ChromaDB của đồ án đạt độ tinh khiết gần như tuyệt đối, giúp AI khi "móc" dữ liệu lên là có ngay câu trả lời chính xác mà không bị vướng tạp chất.
