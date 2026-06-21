import { adminFetch } from './api.js';
import { loadAdminData } from './dataLoader.js';
import { escapeHtml } from './utils.js';

export function setupScrape() {
    const scrapeBtn = document.getElementById('scrape-btn');
    const scrapeStatus = document.getElementById('scrape-status');
    
    if(scrapeBtn) {
        scrapeBtn.addEventListener('click', async () => {
            if (!confirm('Bạn có chắc chắn muốn tải dữ liệu mới từ cổng thông tin TLU không?')) return;
            const scrapeLimitInput = document.getElementById('scrape-limit');
            const limitVal = scrapeLimitInput ? parseInt(scrapeLimitInput.value) : 50;
            const originalText = scrapeBtn.innerHTML;
            scrapeBtn.disabled = true;
            scrapeBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang chạy...';
            scrapeStatus.className = 'status-msg';
            scrapeStatus.style.display = 'block';
            scrapeStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang tải dữ liệu... <b>Vui lòng KHÔNG đóng trình duyệt!</b>';
            try {
                const formData = new FormData();
                formData.append('category', 'all');
                formData.append('limit', limitVal);
                const res = await adminFetch('/api/admin/scrape', { method: 'POST', body: formData });
                const data = await res.json();
                if (data.status === 'success') {
                    scrapeStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(data.message)}`;
                    loadAdminData();
                } else {
                    scrapeStatus.className = 'status-msg error';
                    scrapeStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.message)}`;
                }
            } catch (e) {
                scrapeStatus.className = 'status-msg error';
                scrapeStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Lỗi kết nối khi tải dữ liệu`;
            } finally {
                scrapeBtn.disabled = false;
                scrapeBtn.innerHTML = originalText;
            }
        });
    }
}

export async function checkScrapeStatus() {
    try {
        const res = await adminFetch('/api/admin/scrape/check');
        const data = await res.json();
        const infoEl = document.getElementById('last-crawl-info');
        const btn = document.getElementById('scrape-btn');
        if (data.status === 'success' && infoEl && btn) {
            const last = escapeHtml(data.last_crawl ? data.last_crawl : 'Chưa từng chạy');
            const count = Number(data.new_count) || 0;
            if (count > 0) {
                infoEl.innerHTML = `<span style="color: var(--text-secondary);">Lần crawl cuối: <b>${last}</b></span><br><span style="color: var(--success); font-weight: bold;"><i class="fa-solid fa-bell"></i> Phát hiện ${count} bài viết mới!</span>`;
                btn.style.display = 'inline-block';
                btn.innerHTML = '<i class="fa-solid fa-cloud-download"></i> Cập nhật bài viết';
            } else {
                infoEl.innerHTML = `<span style="color: var(--text-secondary);">Lần crawl cuối: <b>${last}</b></span><br><span style="color: var(--success);"><i class="fa-solid fa-check-circle"></i> Đã cập nhật đầy đủ.</span>`;
                btn.style.display = 'none';
            }
        }
    } catch(e) { console.error(e); }
}
