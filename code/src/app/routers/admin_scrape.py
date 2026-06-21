from fastapi import APIRouter, Depends, Form
from src.config.settings import settings
from src.app.dependencies import get_current_user, logger

router = APIRouter(prefix="/api/admin/scrape", tags=["scrape"])

@router.post("")
def start_scrape(category: str = Form("all"), limit: int = Form(10), current_user: dict = Depends(get_current_user)):
    from src.utils.scraper import TLUAdmissionScraper
    scraper = TLUAdmissionScraper()
    
    try:
        if category == "all":
            for cat in settings.SCRAPER.categories:
                scraper.scrape_category(cat.model_dump(), limit=limit)
        else:
            cat_config = next((c for c in settings.SCRAPER.categories if c.name == category), None)
            if not cat_config:
                return {"status": "error", "message": f"Không tìm thấy category: {category}"}
            scraper.scrape_category(cat_config.model_dump(), limit=limit)
            
        scraper.update_last_crawl()
        logger.info(f"AUDIT: User {current_user['username']} completed Scraping for {category} with limit {limit}")
        return {"status": "success", "message": "Hoàn thành quá trình Scraping!"}
    except Exception as e:
        logger.error(f"AUDIT: User {current_user['username']} encountered Scraping Error: {str(e)}")
        return {"status": "error", "message": f"Lỗi Scraping: {str(e)}"}

@router.get("/check")
def check_scrape_status(current_user: dict = Depends(get_current_user)):
    from src.utils.scraper import TLUAdmissionScraper
    scraper = TLUAdmissionScraper()
    last_crawl = scraper.get_last_crawl()
    new_count = scraper.check_new()
    return {"status": "success", "last_crawl": last_crawl, "new_count": new_count}
