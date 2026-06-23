import { adminFetch } from './api.js';

export function setupTester() {
    const searchBtn = document.getElementById('tester-search-btn');
    const queryInput = document.getElementById('tester-query');
    const resultsContainer = document.getElementById('tester-results');
    const statusDiv = document.getElementById('tester-status');

    if (!searchBtn || !queryInput) return;

    searchBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        if (!query) return;

        searchBtn.disabled = true;
        searchBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang tìm...';
        statusDiv.className = 'status-msg mt-2 d-none';
        resultsContainer.innerHTML = '';

        try {
            const response = await adminFetch(`/api/admin/test_retrieval?query=${encodeURIComponent(query)}`);

            if (!response.ok) throw new Error('API Error');
            
            const data = await response.json();
            
            if (data.results && data.results.length > 0) {
                let html = '';
                data.results.forEach((res, index) => {
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; border-left: 4px solid var(--primary);">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                <strong style="color: var(--primary);">#${index + 1} | Điểm: ${res.score.toFixed(3)}</strong>
                                <span style="font-size: 0.85em; color: var(--text-secondary); background: rgba(255, 255, 255, 0.1); padding: 2px 6px; border-radius: 4px;">Nguồn: ${res.source}</span>
                            </div>
                            <div style="white-space: pre-wrap; font-family: monospace; font-size: 0.9em; background: rgba(0, 0, 0, 0.2); color: var(--text-primary); padding: 10px; border-radius: 4px; border: 1px solid rgba(255, 255, 255, 0.1);">${res.content}</div>
                        </div>
                    `;
                });
                resultsContainer.innerHTML = html;
            } else {
                resultsContainer.innerHTML = '<p class="text-secondary text-center">Không tìm thấy tài liệu phù hợp.</p>';
            }
        } catch (error) {
            statusDiv.textContent = 'Lỗi kết nối. Vui lòng thử lại.';
            statusDiv.className = 'status-msg mt-2 error';
        } finally {
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<i class="fa-solid fa-search"></i> Test Search';
        }
    });

    queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchBtn.click();
    });
}
