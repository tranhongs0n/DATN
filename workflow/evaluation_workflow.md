# Evaluation Workflow (RAGAS)

This document describes how the AI's accuracy and hallucination rates are measured using the RAGAS framework.

## 1. Ground Truth Generation
1. **Dataset**: A golden dataset of question-answer pairs (`ragas_1200_dataset.json`) is maintained. This contains historical admission questions and exactly correct answers verified by admission staff.

## 2. Evaluation Execution
1. **Script Execution**: The developer or admin runs `python tests/evaluate.py`.
2. **Batch Processing**: The script iterates through the golden dataset, submitting each question to the RAG pipeline.
3. **Retrieval**: For each question, the system retrieves relevant chunks from ChromaDB.

## 3. Metric Calculation
RAGAS evaluates the response using the LLM-as-a-judge paradigm across several metrics:
- **Faithfulness**: Are the claims in the generated answer entirely supported by the retrieved context? (Measures hallucination).
- **Answer Relevance**: Does the generated answer directly address the user's question?
- **Context Precision**: Were the most relevant chunks ranked highest in the retrieval?
- **Context Recall**: Did the retrieval find all the information necessary to answer the question?

## 4. Result Analysis
1. **Logging**: The results are exported to `ragas_eval_1200_log.csv`.
2. **Iteration**: If metrics fall below acceptable thresholds (e.g., Faithfulness < 0.9), the team adjusts chunk sizes, overlap, prompts, or the embedding model and re-runs the evaluation.
