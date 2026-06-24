import PyPDF2

def get_toc(filename):
    print(f"--- TOC for {filename} ---")
    try:
        reader = PyPDF2.PdfReader(filename)
        for i in range(min(15, len(reader.pages))):
            text = reader.pages[i].extract_text()
            if "MỤC LỤC" in text.upper() or "MUC LUC" in text.upper():
                print(f"Page {i}:")
                # Print the lines that look like TOC entries
                lines = text.split('\n')
                for line in lines:
                    if "......" in line or "    " in line or "CHƯƠNG" in line.upper():
                        print(line.strip())
                break
    except Exception as e:
        print("Error:", e)

get_toc("Ref/12. Chatbot đa phương tiện hỗ trợ, cố vấn học tập cho sinh viên.pdf")
get_toc("Ref/60TH2_1851061601_Cao Minh Hiếu.2026-01-28-11-10-04.pdf")
get_toc("Ref/64CNTT2_2251061907_Vũ Văn Trung.2026-01-20-09-34-41.pdf")
