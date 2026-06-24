import urllib.request

mermaid_code = """%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'background': '#ffffff'}}}%%
graph TD
    S((Bắt đầu)) --> A[Admin tải file PDF/DOCX]
    A --> B[API tiếp nhận và Lưu tệp tạm]
    B --> C[Bóc tách chữ và bảng biểu (Docling)]
    C --> D[Chuyển đổi sang định dạng Markdown]
    D --> E[RecursiveTextSplitter cắt văn bản 1000 ký tự]
    E --> F[Gửi các chunk lên LLM Embedding API]
    F --> G[Lưu mảng Vector và Metadata vào ChromaDB]
    G --> H[Cập nhật trạng thái hoàn thành vào SQL]
    H --> E2((Kết thúc))
"""

try:
    url = "https://kroki.io/mermaid/png"
    req = urllib.request.Request(
        url, data=mermaid_code.encode("utf-8"), method="POST"
    )
    req.add_header("Content-Type", "text/plain")
    req.add_header("User-Agent", "Mozilla/5.0")
    with urllib.request.urlopen(req, timeout=30) as resp:
        print("Success!")
except Exception as e:
    import urllib.error
    if isinstance(e, urllib.error.HTTPError):
        err_msg = e.read().decode('utf-8')
        with open("kroki_error.txt", "w", encoding="utf-8") as f:
            f.write(err_msg)
    else:
        print(f"FAILED: {e}")
