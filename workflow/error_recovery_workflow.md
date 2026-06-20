# Error Recovery Workflow

This document outlines the standard operating procedures for handling critical system failures.

## 1. Vector Database Corruption
- **Symptom**: System fails to start, or chat queries return ChromaDB instantiation errors.
- **Action**: 
  1. Trigger a full rebuild via the Admin UI. 
  2. If the UI is inaccessible, run `python main.py build-db` via CLI. 
  3. The system will regenerate the vector store from local raw files.

## 2. Zalo Webhook Failures
- **Symptom**: Zalo users receive no response; Zalo OA dashboard shows webhook delivery failures.
- **Action**:
  1. Check the server logs for `429 Rate Limit` errors (user abuse).
  2. Check if the SSL certificate has expired (Zalo requires strict HTTPS).
  3. Check if the Zalo Access Token has expired. If so, run `python src/utils/zalo_token_refresh.py`.

## 3. Gemini API Outages or Quota Exhaustion
- **Symptom**: 503/429 errors from Google API; chatbot replies with system fallback messages.
- **Action**:
  1. The system automatically traps this exception and asks the user to wait for a human consultant.
  2. The Admin receives a notification in the dashboard.
  3. Wait for quota reset or switch to a fallback API key in `.env`.

## 4. Unresponsive Scraper
- **Symptom**: Admin clicks "Scrape" but no new files appear.
- **Action**:
  1. The TLU Admission Portal HTML structure may have changed.
  2. Developer must inspect the DOM structure and update `BeautifulSoup` selectors in `src/utils/scraper.py`.
