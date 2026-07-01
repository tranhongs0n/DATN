import docx
from pathlib import Path
from build_doc import process_content_file

BASE_DIR = Path(r"D:\DATN\thesis")
DOC_PATH = BASE_DIR / "DocOutput" / "DATN_Report_V2.docx"
OUT_PATH = BASE_DIR / "DocOutput" / "DATN_Report_V2_appended.docx"

md_content = """### 3.7.6. Phân hệ quản lý người dùng
Để đảm bảo tính bảo mật của hệ thống, giao diện quản trị cung cấp phân hệ quản lý người dùng. Quản trị viên cấp cao có thể tạo mới, cập nhật, cấp quyền hoặc thu hồi quyền truy cập của các thành viên trong ban tuyển sinh. Các thao tác đều được giám sát và lưu vết để đảm bảo tính minh bạch.

[ CHÈN ẢNH GIAO DIỆN QUẢN LÝ NGƯỜI DÙNG VÀO ĐÂY ]

*Hình 3.7: Giao diện phân hệ quản lý người dùng*

### 3.7.7. Giao diện quản lý từ viết tắt
Trong ngữ cảnh tuyển sinh, học sinh thường sử dụng rất nhiều từ lóng hoặc từ viết tắt (VD: "cntt" thay cho "Công nghệ thông tin"). Giao diện này cho phép quản trị viên định nghĩa và cập nhật linh hoạt từ điển viết tắt. Khi câu hỏi đi vào hệ thống, các từ này sẽ được tự động giải nghĩa trước khi đưa vào luồng tìm kiếm.

[ CHÈN ẢNH GIAO DIỆN QUẢN LÝ TỪ VIẾT TẮT VÀO ĐÂY ]

*Hình 3.8: Giao diện quản lý và định nghĩa từ viết tắt*

### 3.7.8. Kiểm thử tiền xử lý (Query Test)
Mô đun Query Test cho phép quản trị viên xem trước cách thức hệ thống tiền xử lý và nhúng (embedding) câu hỏi. Quản trị viên có thể kiểm tra xem câu hỏi có được giải nghĩa đúng từ viết tắt hay không, và danh sách các đoạn văn bản (chunks) nào sẽ được Vector Database truy xuất lên. Điều này giúp tinh chỉnh cơ sở dữ liệu một cách hiệu quả nhất.

[ CHÈN ẢNH GIAO DIỆN KIỂM THỬ TIỀN XỬ LÝ VÀO ĐÂY ]

*Hình 3.9: Giao diện kiểm thử luồng tiền xử lý câu hỏi (Query Test)*
"""

temp_md = BASE_DIR / "temp_append.md"
with open(temp_md, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Loading {DOC_PATH.name}...")
doc = docx.Document(DOC_PATH)

doc.add_page_break()
p = doc.add_paragraph("--- APPEND TEST ---")
p.style = 'Normal'

mermaid_counter = [10]
process_content_file(doc, temp_md, True, mermaid_counter)

doc.save(OUT_PATH)
print(f"Saved test output to {OUT_PATH}")

if temp_md.exists():
    temp_md.unlink()
