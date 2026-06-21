import { setupAuth } from './auth.js';
import { setupDashboard } from './dashboard.js';
import { setupUsers } from './users.js';
import { setupScrape } from './scrape.js';

document.addEventListener('DOMContentLoaded', () => {
    // Tab logic
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.getAttribute('data-tab')).classList.add('active');
        });
    });

    // View logic
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const adminView = document.getElementById('admin-view');
    if (adminView) adminView.classList.add('active');

    // Setup all modules
    setupDashboard();
    setupUsers();
    setupScrape();
    
    // Auth must be last since it checks token and loads data
    setupAuth();
});
