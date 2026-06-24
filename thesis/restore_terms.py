import os
import glob

replacements = {
    'cơ sở dữ liệu vector': 'Vector Database',
    'bộ nhớ đệm ngữ nghĩa': 'Semantic Cache',
    'thuật toán phân rã tài liệu cố định theo độ dài': 'RecursiveCharacterTextSplitter',
    'công cụ phân rã theo kích thước ký tự': 'RecursiveCharacterTextSplitter',
    'động cơ đa phương thức': 'MultimodalEngine',
    'cơ chế chờ kết nối dài hạn': 'Long Polling',
    'thuật toán bẫy lỗi từ chối dịch vụ': 'Rate Limit Backoff',
    'kết nối dòng sự kiện liên tục': 'Server-Sent Events (SSE)',
    'truyền tải dòng sự kiện liên tục': 'Server-Sent Events (SSE)',
    'bảng điều khiển web': 'Web Admin Dashboard',
    'bảng điều khiển quản trị viên': 'Web Admin Dashboard',
    'bảng điều khiển quản trị': 'Web Admin Dashboard',
    'phân hệ cào dữ liệu tự động': 'Web Scraper',
    'công cụ cào dữ liệu': 'Web Scraper',
    'thu thập dữ liệu đa luồng': 'Web Scraper đa luồng',
    'thu thập dữ liệu tự trị': 'Autonomous Agent Scraper',
    'nền tảng đa tác vụ': 'Multi-Agent',
    'tự động hóa toàn phần': 'RPA (Robotic Process Automation)',
    'hiện tượng bịa đặt thông tin': 'hiện tượng ảo giác (Hallucination)',
    'chống bịa đặt thông tin': 'chống Hallucination',
    'xung đột tri thức': 'Knowledge Conflict',
    'mô hình vi dịch vụ': 'Microservices',
    'mở rộng theo chiều ngang': 'Horizontal Scaling',
    'mô hình ngôn ngữ lớn': 'LLM',
    'mô hình ngôn ngữ': 'LLM',
    'trí tuệ nhân tạo': 'AI',
    'tấn công vét cạn': 'Brute-force',
    'tấn công bằng bảng băm tính trước': 'Rainbow Table',
    'chuỗi ngẫu nhiên phụ trợ': 'Salt',
    'mã thông báo chuẩn JWT không lưu trạng thái': 'JWT stateless',
    'chuỗi mã thông báo chuẩn JWT': 'JWT',
    'phân hệ quản trị tài khoản chuyên biệt': 'User Management Module',
    'cơ sở dữ liệu cục bộ': 'Local Database',
    'ứng dụng đồ thị tri thức': 'kiến trúc GraphRAG',
    'kiến trúc đồ thị tri thức': 'kiến trúc GraphRAG',
    'phép toán đại số tuyến tính': 'Dot product và Norm',
    'công cụ ghi nhật ký': 'Audit Logging',
    'độ chuẩn xác ngữ cảnh': 'Context Precision',
    'độ phủ ngữ cảnh': 'Context Recall',
    'độ trung thực để chống bịa đặt thông tin': 'Faithfulness (Độ trung thực)',
    'độ liên quan của câu trả lời': 'Answer Relevancy',
    'Độ chuẩn xác': 'Context Precision',
    'Độ trung thực': 'Faithfulness',
    'Độ liên quan': 'Answer Relevancy',
    'hiệu ứng đối thoại thời gian thực': 'Streaming',
    'dòng sự kiện liên tục': 'Server-Sent Events (SSE)',
    'cơ chế chia sẻ tài nguyên chéo nguồn gốc': 'CORS Middleware',
    'điểm dữ liệu': 'Points',
    'thực thể liên kết': 'ERD',
    'phân rã theo kích thước cố định': 'Phân rã theo kích thước cố định (Fixed-size Chunking)',
    'phân rã đệ quy': 'Phân rã đệ quy (Recursive Chunking)',
    'phân rã theo ngữ nghĩa': 'Phân rã theo ngữ nghĩa (Semantic Chunking)',
    'truy xuất và sinh văn bản đầu cuối': 'End-to-End RAG',
    'ngữ cảnh rời rạc trong mệnh đề điều kiện': 'ngữ cảnh rời rạc (Chunking Conflict)'
}

for filepath in glob.glob('D:/DATN/thesis/Document_Planing/Content/*.md'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for k, v in replacements.items():
        # case-insensitive replacement might be tricky, we will do exact matches but also capitalize first letter
        content = content.replace(k, v)
        content = content.replace(k.capitalize(), v)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated translations in all MD files.')
