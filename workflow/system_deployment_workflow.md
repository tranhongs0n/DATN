# System Deployment Workflow

This document outlines the end-to-end process for deploying the TLU Admission RAG Assistant from scratch.

## 1. Environment Preparation
1. **Server Requirements**: Linux VM (Ubuntu recommended), Python 3.10+, minimum 4GB RAM.
2. **Clone Repository**: Clone the DATN repository to the target server.
3. **Virtual Environment**: 
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

## 2. External Services Setup
1. **Google Gen AI API**:
   - Generate a Gemini API key from Google AI Studio.
2. **Zalo Official Account (OA)**:
   - Register a Zalo OA for the university.
   - Create a Zalo App and link it to the OA.
   - Generate App ID, Secret Key, Access Token, and Refresh Token.

## 3. Configuration Configuration
1. **Environment Variables**:
   - Copy `.env.example` to `.env`.
   - Fill in `GOOGLE_API_KEY`, `ZALO_ACCESS_TOKEN`, `ZALO_APP_ID`, `ZALO_SECRET_KEY`, `ZALO_REFRESH_TOKEN`.
2. **Admin Setup**:
   - The first run of the system will automatically create the `admin` SQLite database (`auth.db`) with a default admin account.

## 4. Initial Data Bootstrapping
1. **Start System**: Run the backend API server.
2. **Scraping**: Admin uses the dashboard to trigger an initial web scrape of the TLU Admission portal to gather base documents.
3. **Indexing**: Admin triggers the first Vector DB Rebuild.

## 5. Webhook Registration
1. **Expose Server**: Use a reverse proxy (like Nginx) and SSL (Let's Encrypt) to expose the server securely over HTTPS.
2. **Zalo Developer Portal**: 
   - Set the Webhook URL in the Zalo App to `https://<your-domain>/zalo/webhook`.
   - Subscribe to the `user_send_text` event.
