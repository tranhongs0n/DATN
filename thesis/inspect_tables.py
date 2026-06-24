import docx

doc = docx.Document("HoangThaiDuy_DATN.docx")
print("Tables in document:")
for i, t in enumerate(doc.tables):
    if i > 5: break
    print(f"\n--- Table {i} ---")
    for row in t.rows:
        row_data = [cell.text.strip() for cell in row.cells]
        print(" | ".join(row_data))
