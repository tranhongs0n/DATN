export function getToken() {
    return localStorage.getItem('authToken');
}
export function setToken(token) {
    if (token) localStorage.setItem('authToken', token);
    else localStorage.removeItem('authToken');
}
export async function adminFetch(url, options = {}) {
    let token = getToken();
    if (!options.headers) options.headers = {};
    if (token) options.headers['Authorization'] = 'Bearer ' + token;
    
    const res = await fetch(url, options);
    if (res.status === 401) {
        setToken(null);
        document.getElementById('login-modal').classList.add('active');
        throw new Error('Unauthorized');
    }
    return res;
}
