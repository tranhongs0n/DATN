# Maintenance Workflow

This document outlines periodic tasks required to keep the system running smoothly.

## 1. Zalo Token Refresh (Weekly/Monthly)
- **Why**: Zalo Access Tokens expire periodically.
- **Process**:
  - Run `python src/utils/zalo_token_refresh.py`.
  - The script uses the Refresh Token to negotiate a new Access Token.
  - *Automation*: This script should be added to a system `cron` job to run automatically every 7 days.

## 2. Content Updates (As Needed)
- **Why**: Admission policies and scores change yearly.
- **Process**:
  - Admin logs into the dashboard and uploads the new official PDF decrees.
  - Admin clicks "Rebuild Database".
  - The old information is purged, and the AI will only retrieve facts from the newly uploaded documents.

## 3. Chat History Archiving (Quarterly)
- **Why**: `chat_history.db` will grow large over time, slowing down queries.
- **Process**:
  - Admin clicks the "Export Chat Data" endpoint (`/api/admin/export/chats`) to download the CSV.
  - The IT team can safely archive and truncate the `messages` table for records older than 1 year to preserve performance.

## 4. Software Dependencies (Quarterly)
- **Why**: LangChain, Chroma, and Google Gen AI SDK update frequently.
- **Process**:
  - Test updates in a staging environment.
  - Run `pip install -U -r requirements.txt` (or update `pyproject.toml`).
  - Run the RAGAS Evaluation script to ensure accuracy hasn't degraded with the new library versions.
