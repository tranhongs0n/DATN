import { adminFetch, setToken, getToken } from './api.js';
import { loadAdminData } from './dataLoader.js';

export function setupAuth() {
    const loginForm = document.getElementById('login-form');
    const loginUsername = document.getElementById('login-username');
    const loginPassword = document.getElementById('login-password');
    const loginError = document.getElementById('login-error');
    const logoutBtn = document.getElementById('logout-btn');
    const loginModal = document.getElementById('login-modal');

    if(loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            loginError.style.display = 'none';
            
            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: loginUsername.value, password: loginPassword.value })
                });
                const data = await res.json();
                
                if (res.ok && data.status === 'success') {
                    setToken(data.token);
                    loginModal.classList.remove('active');
                    loginForm.reset();
                    loadAdminData();
                } else {
                    loginError.textContent = data.detail || 'Login failed';
                    loginError.style.display = 'block';
                }
            } catch (err) {
                loginError.textContent = 'Connection error';
                loginError.style.display = 'block';
            }
        });
    }

    if(logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            const token = getToken();
            if (token) {
                try {
                    await adminFetch('/api/auth/logout', { method: 'POST' });
                } catch (e) {}
                setToken(null);
            }
            loginModal.classList.add('active');
            window.location.href = '/';
        });
    }

    if (!getToken()) {
        if(loginModal) loginModal.classList.add('active');
    } else {
        if(loginModal) loginModal.classList.remove('active');
        setTimeout(loadAdminData, 0);
    }
}
