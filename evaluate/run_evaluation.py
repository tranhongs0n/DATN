import os
import sys
import json
import logging
import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'codebase')))

from src.core.vector_db import VectorDBManager
from src.core.multimodal import MultimodalEngine
from src.config.settings import settings

INPUT_DATASET_CSV = "dataset.csv"
OUTPUT_RESULTS_CSV = "evaluation_results.csv"
ENV_PATH = "../codebase/.env"

EVAL_LLM_MODEL = "gemini-1.5-flash"
EVAL_EMBEDDING_MODEL = "models/text-embedding-004"

CHROMA_SEARCH_K = 3
BM25_SEARCH_K = 3
RRF_K = 60
BM25_WEIGHT = 0.4
CHROMA_WEIGHT = 0.6
FINAL_TOP_K = 4

logger = logging.getLogger(__name__)

def load_test_data(csv_path=INPUT_DATASET_CSV):
    df = pd.read_csv(csv_path)
    return df.to_dict('records')

def run_retrieval_and_generation():
    print("Initializing RAG system for generation...")
    db_manager = VectorDBManager()
    engine = MultimodalEngine()
    
    db = db_manager.get_db()
    bm25 = db_manager.get_bm25_retriever()
    if not db:
        print("Error: Vector DB not initialized.")
        return None
        
    chroma_retriever = db.as_retriever(search_kwargs={"k": CHROMA_SEARCH_K})
    
    samples = load_test_data()
    results = []
    
    total = len(samples)
    for idx, sample in enumerate(samples):
        question = sample["question"]
        ground_truth = sample["ground_truth"]
        
        if bm25:
            bm25.k = BM25_SEARCH_K
            docs_bm25 = bm25.invoke(question)
            docs_chroma = chroma_retriever.invoke(question)
            
            doc_scores = {}
            for rank, doc in enumerate(docs_bm25):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + BM25_WEIGHT / (rank + RRF_K)
            for rank, doc in enumerate(docs_chroma):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + CHROMA_WEIGHT / (rank + RRF_K)
                
            all_docs = {doc.page_content: doc for doc in docs_bm25 + docs_chroma}
            docs = [all_docs[content] for content, _ in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)]
            docs = docs[:FINAL_TOP_K]
        else:
            docs = chroma_retriever.invoke(question)
            
        contexts = [d.page_content for d in docs]
        
        chatbot_prompts = settings.PROMPTS.get("chatbot", {})
        prefix = chatbot_prompts.get("context_prefix", "Thông tin tham khảo:")
        
        from datetime import datetime
        current_year = datetime.now().year
        context_parts = [f"THÔNG TIN HỆ THỐNG: Năm hiện tại là {current_year}."]
        for d in docs:
            source = d.metadata.get("source", "Không rõ nguồn") if d.metadata else "Không rõ nguồn"
            filename = os.path.basename(source)
            context_parts.append(f"[Nguồn: {filename}]\n{d.page_content}")
            
        context_str = f"\n\n{prefix}\n" + "\n---\n".join(context_parts)
        
        template = chatbot_prompts.get("query_template", "{context}\n\n{message}")
        prompt = template.format(context=context_str, message=question)
        
        full_response = ""
        for chunk in engine.query_stream([], prompt):
            full_response += chunk
            
        results.append({
            "question": question,
            "contexts": contexts,
            "answer": full_response,
            "ground_truth": ground_truth
        })
        if (idx + 1) % 10 == 0:
            print(f"Processed {idx+1}/{total}")
        
    return results

def run_evaluation():
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import (
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
        )
        from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    except ImportError:
        print("Error: Missing required libraries.")
        return

    load_dotenv(dotenv_path=ENV_PATH)
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not set.")
        return
        
    print("STEP 1: RETRIEVAL AND GENERATION")
    results = run_retrieval_and_generation()
    if not results:
        return
        
    data = {
        "question": [r["question"] for r in results],
        "answer": [r["answer"] for r in results],
        "contexts": [r["contexts"] for r in results],
        "ground_truth": [r["ground_truth"] for r in results]
    }
    
    dataset = Dataset.from_dict(data)
    
    print("STEP 2: RAGAS EVALUATION")
    
    gemini_llm = ChatGoogleGenerativeAI(model=EVAL_LLM_MODEL)
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model=EVAL_EMBEDDING_MODEL)
    
    print(f"Running evaluation on {len(results)} samples...")
    
    try:
        eval_result = evaluate(
            dataset=dataset,
            metrics=[
                context_precision,
                context_recall,
                faithfulness,
                answer_relevancy,
            ],
            llm=gemini_llm,
            embeddings=gemini_embeddings,
            raise_exceptions=True
        )
        
        print("EVALUATION RESULTS:")
        print(eval_result)
        
        df = eval_result.to_pandas()
        df.to_csv(OUTPUT_RESULTS_CSV, index=False)
        print(f"Results saved to {OUTPUT_RESULTS_CSV}")
        
    except Exception as e:
        print(f"Evaluation error: {e}")

if __name__ == "__main__":
    run_evaluation()
