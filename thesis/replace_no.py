import glob

replacements = {
    'nó bộc lộ điểm yếu ở tính tĩnh tại': 'kiến trúc này bộc lộ điểm yếu ở tính tĩnh tại',
    'nó chỉ so khớp xác suất văn bản': 'mô hình chỉ so khớp xác suất văn bản',
    'nó không có khả năng tự động sinh ra': 'hệ thống không có khả năng tự động sinh ra',
    'Mục tiêu của nó ở giai đoạn này': 'Mục tiêu của mô hình ở giai đoạn này',
    'Nó học cách phản hồi lại': 'Mô hình học cách phản hồi lại',
    'nó không có khái niệm biết hay không': 'LLM không có khái niệm biết hay không',
    'nó sẽ sinh ra một con số ngẫu nhiên': 'mô hình sẽ sinh ra một con số ngẫu nhiên',
    'nó hoàn tất huấn luyện. Nó không thể biết': 'quá trình huấn luyện hoàn tất. Mô hình không thể biết',
    'nó sẽ đệ quy cắt theo câu': 'thuật toán sẽ đệ quy cắt theo câu',
    'Nó bóc tách các bài viết': 'Phân hệ này bóc tách các bài viết'
}

for filepath in glob.glob('D:/DATN/thesis/Document_Planing/Content/*.md'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for k, v in replacements.items():
        content = content.replace(k, v)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated informal pronoun "nó" in MD files.')
