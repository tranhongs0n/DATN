import argparse
import logging
import sys

from src.utils.scraper import TLUAdmissionScraper
from src.core.vector_db import VectorDBManager
from src.core.indexing import IndexingService
from src.utils.document_loader import DocumentLoader
from src.config.settings import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("DATN-Main")

def run_ui(args):
    import uvicorn
    logger.info(f"Starting FastAPI UI on port {args.port}...")
    uvicorn.run("src.app.api:app", host="0.0.0.0", port=args.port, reload=True)

def run_scrape(args):
    logger.info("Starting Scraper...")
    scraper = TLUAdmissionScraper()
    for cat in settings.CATEGORIES:
        scraper.scrape_category(cat, limit=args.limit)
    logger.info("Scraping complete.")

def run_build_db(args):
    logger.info("Building Vector DB...")
    
    db_manager = VectorDBManager()
    loader = DocumentLoader()
    indexing_service = IndexingService(db_manager, loader)
    
    docs = []

    if args.files:
        logger.info(f"Indexing specific files: {args.files}")
        docs = indexing_service.load_files_by_path(args.files)
    else:
        logger.info("Loading all documents from data directory...")
        docs = indexing_service.load_all_from_disk()
    
    if args.limit:
        logger.info(f"Limiting to first {args.limit} documents.")
        docs = docs[:args.limit]

    if not docs:
        logger.error("No documents found to index.")
        return
        
    db_manager.build_from_documents(docs, append=args.append)
    logger.info("Vector DB build complete.")

def main():
    parser = argparse.ArgumentParser(description="DATN - Tuyển sinh TLU RAG CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # UI Command
    ui_parser = subparsers.add_parser("ui", help="Launch the Modern FastAPI Chat & Admin UI")
    ui_parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")

    # Scrape Command
    scrape_parser = subparsers.add_parser("scrape", help="Run the web scraper")
    scrape_parser.add_argument("--limit", type=int, default=None, help="Limit articles per category")

    # Build DB Command
    db_parser = subparsers.add_parser("build-db", help="Build the Chroma vector database")
    db_parser.add_argument("--files", nargs="+", help="Specific files to index")
    db_parser.add_argument("--limit", type=int, help="Limit number of documents to index")
    db_parser.add_argument("--append", action="store_true", help="Append to existing database instead of rebuilding")

    args = parser.parse_args()
    
    if args.command == "ui":
        run_ui(args)
    elif args.command == "scrape":
        run_scrape(args)
    elif args.command == "build-db":
        run_build_db(args)
    elif not args.command:
        run_ui(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
