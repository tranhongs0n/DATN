import docx

doc = docx.Document("Ref/HoangThaiDuy_DATN.docx")
for i, table in enumerate(doc.tables):
    if len(table.rows) > 0:
        row_data = [cell.text.strip() for cell in table.rows[0].cells]
        print(f"Table {i}: {' | '.join(row_data)[:100]}")
