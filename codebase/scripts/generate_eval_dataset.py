import os
import sys
import json
import random
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.vector_db import VectorDBManager
from src.config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY") or settings.GOOGLE_API_KEY
if not api_key:
    print("No GOOGLE_API_KEY found in .env")
    exit(1)


llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", google_api_key=api_key)

PROMPT_TEMPLATE = """
Dựa vào đoạn văn bản sau, hãy tạo ra 5 cặp Câu hỏi - Câu trả lời (Q&A) tương ứng với 5 nhóm đánh giá khác nhau.
Chú ý: Câu trả lời phải hoàn toàn dựa trên đoạn văn bản được cung cấp. Không bịa đặt thông tin.

Đoạn văn bản:
{chunk}

5 nhóm đánh giá bao gồm:
1. Tra cứu cơ bản: Câu hỏi trực tiếp về thông tin cụ thể (mã ngành, điểm chuẩn, v.v.).
2. Ngôn ngữ thực tế: Câu hỏi dùng tiếng Việt không dấu, viết tắt, hoặc ngôn ngữ gen Z mạng xã hội.
3. Suy luận logic: Câu hỏi yêu cầu tổng hợp hoặc kết nối 2-3 dữ kiện từ đoạn văn để trả lời.
4. Bẫy ngoài phạm vi: Câu hỏi hỏi về thông tin KHÔNG CÓ trong văn bản, câu trả lời phải là "Không có thông tin".
5. Đa bậc đào tạo: Câu hỏi cố tình gây nhầm lẫn giữa đại học và thạc sĩ/tiến sĩ.

Trả về kết quả dưới định dạng JSON array với các trường: "group" (tên nhóm 1-5), "question" (câu hỏi), "answer" (câu trả lời).
Không thêm markdown hay text nào khác ngoài JSON.
"""

def generate_dataset(output_file, target_count=1200):
    db_manager = VectorDBManager()
    db = db_manager.get_db()
    if not db:
        print("Không tìm thấy VectorDB.")
        return

    data = db.get()
    chunks = data['documents']
    sources = data['metadatas']
    
    if not chunks:
        print("VectorDB trống.")
        return
        
    print(f"Loaded {len(chunks)} chunks from DB.")
    

    combined = list(zip(chunks, sources))
    random.shuffle(combined)
    
    dataset = []
    

    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
            print(f"Resuming from {len(dataset)} existing Q&A pairs.")

    chunks_needed = (target_count - len(dataset)) // 5 + 1
    if chunks_needed <= 0:
        print("Đã đủ số lượng câu hỏi yêu cầu!")
        return
        
    for i, (chunk, meta) in enumerate(combined):
        if len(dataset) >= target_count:
            break
            
        print(f"Processing chunk {i+1}... (Current dataset size: {len(dataset)})")
        
        prompt = PROMPT_TEMPLATE.format(chunk=chunk)
        try:
            response = llm.invoke(prompt)
            text = response.content.strip()
            if text.startswith('```json'):
                text = text[7:-3].strip()
            elif text.startswith('```'):
                text = text[3:-3].strip()
                
            qas = json.loads(text)
            
            for qa in qas:
                qa['source'] = meta.get('source', 'Unknown')
                dataset.append(qa)
                

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, ensure_ascii=False, indent=4)
                
            time.sleep(2)
            
        except Exception as e:
            print(f"Error on chunk {i+1}: {e}")
            time.sleep(5)
            
    print(f"Completed! Total {len(dataset)} Q&A pairs saved to {output_file}.")

if __name__ == "__main__":
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'thesis', 'Document_Planing', 'Evaluation', 'ground_truth.json'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    generate_dataset(out_path, target_count=1200)
