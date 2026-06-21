import { adminFetch } from './api.js';
import { loadAdminData } from './dataLoader.js';

export function setupUsers() {
    const addUserBtn = document.getElementById('add-user-btn');
    const userModalForm = document.getElementById('user-modal-form');
    const cancelUserBtn = document.getElementById('cancel-user-btn');

    if(addUserBtn) {
        addUserBtn.addEventListener('click', () => {
            document.getElementById('user-modal-title').innerHTML = '<i class="fa-solid fa-user-plus"></i> Thêm người dùng';
            document.getElementById('user-modal-id').value = '';
            document.getElementById('user-modal-username').value = '';
            document.getElementById('user-modal-password').value = '';
            document.getElementById('user-modal-password').required = true;
            document.getElementById('user-modal-error').style.display = 'none';
            document.getElementById('user-modal').classList.add('active');
        });
    }

    if(cancelUserBtn) {
        cancelUserBtn.addEventListener('click', () => {
            document.getElementById('user-modal').classList.remove('active');
        });
    }

    if(userModalForm) {
        userModalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            document.getElementById('user-modal-error').style.display = 'none';
            const id = document.getElementById('user-modal-id').value;
            const username = document.getElementById('user-modal-username').value;
            const password = document.getElementById('user-modal-password').value;
            try {
                let res;
                if (id) {
                    res = await adminFetch(`/api/admin/users/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password: password || null })
                    });
                } else {
                    res = await adminFetch('/api/admin/users', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                }
                const data = await res.json();
                if (res.ok && data.status === 'success') {
                    document.getElementById('user-modal').classList.remove('active');
                    loadAdminData();
                } else {
                    document.getElementById('user-modal-error').textContent = data.detail || 'Lỗi lưu người dùng';
                    document.getElementById('user-modal-error').style.display = 'block';
                }
            } catch (err) {
                document.getElementById('user-modal-error').textContent = 'Lỗi kết nối';
                document.getElementById('user-modal-error').style.display = 'block';
            }
        });
    }
}

export async function loadUsers() {
    const usersTableBody = document.querySelector('#users-table tbody');
    if(!usersTableBody) return;
    try {
        const res = await adminFetch('/api/admin/users');
        const users = await res.json();
        usersTableBody.innerHTML = '';
        if (users.users && users.users.length) {
            users.users.forEach((u, index) => {
                const tmpl = document.getElementById('user-row-template').content.cloneNode(true);
                tmpl.querySelector('.user-stt').textContent = index + 1;
                tmpl.querySelector('.user-username').textContent = u.username;
                const roleSpan = tmpl.querySelector('.user-role');
                roleSpan.textContent = u.role;
                if(u.role === 'admin') roleSpan.classList.add('success');
                const editBtn = tmpl.querySelector('.edit-user-btn');
                editBtn.dataset.id = u.id;
                editBtn.dataset.username = u.username;
                editBtn.addEventListener('click', () => {
                    document.getElementById('user-modal-title').innerHTML = '<i class="fa-solid fa-user-pen"></i> Sửa người dùng';
                    document.getElementById('user-modal-id').value = u.id;
                    document.getElementById('user-modal-username').value = u.username;
                    document.getElementById('user-modal-password').value = '';
                    document.getElementById('user-modal-password').required = false;
                    document.getElementById('user-modal-error').style.display = 'none';
                    document.getElementById('user-modal').classList.add('active');
                });
                const delBtn = tmpl.querySelector('.delete-user-btn');
                delBtn.dataset.id = u.id;
                delBtn.addEventListener('click', async () => {
                    if (!confirm('Bạn có chắc chắn muốn xóa người dùng này?')) return;
                    try {
                        const r = await adminFetch(`/api/admin/users/${u.id}`, { method: 'DELETE' });
                        const d = await r.json();
                        if (r.ok && d.status === 'success') loadAdminData();
                        else alert('Lỗi xóa người dùng: ' + (d.detail || d.message));
                    } catch (err) { alert('Lỗi kết nối khi xóa người dùng'); }
                });
                usersTableBody.appendChild(tmpl);
            });
        } else {
            usersTableBody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 2rem;">Không có người dùng.</td></tr>`;
        }
    } catch(e) { console.error(e); }
}
