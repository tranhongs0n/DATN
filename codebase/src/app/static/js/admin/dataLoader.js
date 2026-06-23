import { loadStats, loadFiles, loadUnsupportedFiles } from './dashboard.js';
import { loadUsers } from './users.js';
import { checkScrapeStatus } from './scrape.js';
import { loadAbbreviations } from './abbreviations.js';

let isLoading = false;
export async function loadAdminData() {
    if (isLoading) return;
    isLoading = true;
    try {
        await Promise.all([
            loadStats(),
            loadFiles(),
            loadUnsupportedFiles(),
            loadUsers(),
            checkScrapeStatus(),
            loadAbbreviations()
        ]);
    } catch (e) {
        console.error("Error loading admin data:", e);
    } finally {
        isLoading = false;
    }
}
