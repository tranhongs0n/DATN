import docx

doc = docx.Document("DocOutput/DATN_Report_PhuLuc.docx")

replacements = {
    222: "Hình 2.4: Sơ đồ luồng cập nhật tài liệu và tri thức",
    226: "Hình 2.5: Sơ đồ luồng thu thập dữ liệu tự động từ trang chủ",
    231: "Hình 2.6: Sơ đồ chu trình tư vấn hỏi đáp đa lượt",
    236: "Hình 2.7: Sơ đồ luồng xử lý đa phương thức"
}

for idx, new_text in replacements.items():
    p = doc.paragraphs[idx]
    if "[Missing subtitle]" in p.text:
        p.text = new_text
        p.style = "Hình"
        
doc.save("DocOutput/DATN_Report_PhuLuc.docx")
print("Added subtitles successfully. Saved to DATN_Report_Subtitle.docx")
