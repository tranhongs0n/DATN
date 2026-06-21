import { adminFetch } from './api.js';
import { loadAdminData } from './dataLoader.js';
import { escapeHtml } from './utils.js';

export function setupDashboard() {
    const rebuildBtn = document.getElementById('rebuild-btn');
    const actionStatus = document.getElementById('action-status');
    const fileUpload = document.getElementById('file-upload');
    const bulkConvertBtn = document.getElementById('bulk-convert-btn');

    if(rebuildBtn) {
        rebuildBtn.addEventListener('click', async () => {
            if(!confirm('Bạn có chắc chắn muốn xây dựng lại toàn bộ Index? Thao tác này có thể mất nhiều thời gian và ghi đè dữ liệu cũ.')) return;
            actionStatus.className = 'status-msg';
            actionStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang xây dựng lại Index...';
            try {
                const res = await adminFetch('/api/admin/index/rebuild', { method: 'POST' });
                const data = await res.json();
                if (data.status === 'success') {
                    actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(data.message)}`;
                    alert(`Thành công: ${data.message}`);
                    loadAdminData();
                } else {
                    actionStatus.className = 'status-msg error';
                    actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.message)}`;
                    alert(`Lỗi: ${data.message}`);
                }
            } catch (e) {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Error rebuilding index`;
                alert('Lỗi kết nối khi xây dựng lại Index!');
            }
        });
    }

    if(fileUpload) {
        fileUpload.addEventListener('change', async (e) => {
            const files = e.target.files;
            if (!files.length) return;
            const allowed = ['.pdf', '.docx', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'];
            for (const file of files) {
                const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
                if (!allowed.includes(ext)) {
                    alert(`Tệp ${file.name} không được hỗ trợ!`);
                    e.target.value = '';
                    return;
                }
            }
            const formData = new FormData();
            for (const file of files) formData.append('files', file);

            actionStatus.className = 'status-msg';
            actionStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang tải lên & Index...';
            try {
                const res = await adminFetch('/api/admin/index/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (data.status === 'success') {
                    actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(data.message)}`;
                    alert(`Tải lên thành công: ${data.message}`);
                    loadAdminData();
                } else {
                    actionStatus.className = 'status-msg error';
                    actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.message)}`;
                    alert(`Lỗi tải lên: ${data.message}`);
                }
            } catch (err) {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Upload failed`;
                alert('Lỗi kết nối khi tải lên!');
            }
        });
    }

    if(bulkConvertBtn) {
        bulkConvertBtn.addEventListener('click', async () => {
            const originalText = bulkConvertBtn.innerHTML;
            bulkConvertBtn.disabled = true;
            bulkConvertBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang xử lý...';
            actionStatus.className = 'status-msg';
            actionStatus.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles fa-bounce"></i> Starting bulk conversion...';
            try {
                const res = await adminFetch('/api/admin/files/convert-all', { method: 'POST' });
                const data = await res.json();
                if (data.status === 'success' || data.status === 'warning') {
                    actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(data.message)}`;
                    alert(`Thành công: ${data.message}`);
                    loadAdminData();
                } else {
                    actionStatus.className = 'status-msg error';
                    actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.message)}`;
                    alert(`Lỗi chuyển đổi: ${data.message}`);
                }
            } catch (e) {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Bulk conversion failed`;
                alert('Lỗi kết nối khi chuyển đổi!');
            } finally {
                bulkConvertBtn.disabled = false;
                bulkConvertBtn.innerHTML = originalText;
            }
        });
    }
}

export async function loadStats() {
    const statsContent = document.getElementById('stats-content');
    if(!statsContent) return;
    try {
        const res = await adminFetch('/api/admin/stats');
        const stats = await res.json();
        statsContent.innerHTML = '';
        const tmpl = document.getElementById('stats-template').content.cloneNode(true);
        tmpl.querySelector('.doc-count').textContent = stats.doc_count;
        tmpl.querySelector('.chunk-count').textContent = stats.chunk_count;
        tmpl.querySelector('.embedding-model').textContent = stats.embedding_model;
        tmpl.querySelector('.llm-model').textContent = stats.llm_model;
        statsContent.appendChild(tmpl);
    } catch(e) {
        statsContent.innerHTML = '<div class="status-msg error">Lỗi tải dữ liệu.</div>';
    }
}

export async function loadFiles() {
    const filesTableBody = document.querySelector('#files-table tbody');
    if(!filesTableBody) return;
    try {
        const res = await adminFetch('/api/admin/files');
        const files = await res.json();
        filesTableBody.innerHTML = '';
        if (files.files && files.files.length) {
            files.files.sort((a, b) => {
                const aIdx = (a.status === 'Indexed' || a.status === 'Đã Index') ? 1 : 0;
                const bIdx = (b.status === 'Indexed' || b.status === 'Đã Index') ? 1 : 0;
                return aIdx - bIdx;
            });
            files.files.forEach(f => {
                const tmpl = document.getElementById('file-row-template').content.cloneNode(true);
                tmpl.querySelector('.file-name').textContent = f.name;
                const statusSpan = tmpl.querySelector('.file-status');
                statusSpan.textContent = f.status === 'Indexed' ? 'Đã Index' : f.status === 'Pending' ? 'Chưa Index' : f.status;
                statusSpan.style.color = (f.status === 'Indexed' || f.status === 'Đã Index') ? 'var(--success)' : 'var(--text-secondary)';
                tmpl.querySelector('.file-path').textContent = f.path;
                const indexBtn = tmpl.querySelector('.index-btn');
                const deleteBtn = tmpl.querySelector('.delete-btn');
                if (f.status === 'Indexed' || f.status === 'Đã Index') {
                    indexBtn.disabled = true;
                    indexBtn.innerHTML = '<i class="fa-solid fa-check"></i> Đã Index';
                    indexBtn.classList.replace('primary', 'secondary');
                } else {
                    indexBtn.dataset.file = f.name;
                    indexBtn.addEventListener('click', () => indexSingleFile(f.name, indexBtn));
                }
                deleteBtn.dataset.file = f.name;
                deleteBtn.addEventListener('click', () => deleteSingleFile(f.name, deleteBtn));
                filesTableBody.appendChild(tmpl);
            });
        } else {
            filesTableBody.innerHTML = `<tr><td colspan="4" style="text-align: center; padding: 2rem;">Chưa có tệp nào. Thêm tệp vào thư mục data.</td></tr>`;
        }
    } catch(e) { console.error(e); }
}

export async function loadUnsupportedFiles() {
    const unsupportedTableBody = document.querySelector('#unsupported-table tbody');
    if(!unsupportedTableBody) return;
    try {
        const res = await adminFetch('/api/admin/files/unsupported');
        const unsupported = await res.json();
        unsupportedTableBody.innerHTML = '';
        if (unsupported.files && unsupported.files.length) {
            unsupported.files.forEach(f => {
                const tmpl = document.getElementById('unsupported-file-row-template').content.cloneNode(true);
                tmpl.querySelector('.file-name').textContent = f.name;
                tmpl.querySelector('.file-extension').textContent = f.extension;
                const convertBtn = tmpl.querySelector('.convert-btn');
                const deleteBtn = tmpl.querySelector('.delete-btn');
                convertBtn.dataset.file = f.name;
                convertBtn.addEventListener('click', () => convertSingleFile(f.name, convertBtn));
                deleteBtn.dataset.file = f.name;
                deleteBtn.addEventListener('click', () => deleteSingleFile(f.name, deleteBtn));
                unsupportedTableBody.appendChild(tmpl);
            });
        } else {
            unsupportedTableBody.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 2rem;">Không có tệp cần chuyển đổi.</td></tr>`;
        }
    } catch(e) { console.error(e); }
}

async function convertSingleFile(filename, btnElement) {
    const originalContent = btnElement.innerHTML;
    btnElement.disabled = true;
    btnElement.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang chuyển đổi...';
    const actionStatus = document.getElementById('action-status');
    try {
        const res = await adminFetch('/api/admin/files/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename })
        });
        const data = await res.json();
        if (data.status === 'success') {
            if(actionStatus) {
                actionStatus.className = 'status-msg';
                actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(data.message)}`;
            }
            alert(`Chuyển đổi thành công: ${data.message}`);
            loadAdminData();
        } else {
            if(actionStatus) {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.message)}`;
            }
            alert(`Lỗi chuyển đổi: ${data.message}`);
            btnElement.disabled = false;
            btnElement.innerHTML = originalContent;
        }
    } catch (err) {
        if(actionStatus) {
            actionStatus.className = 'status-msg error';
            actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Conversion failed`;
        }
        alert('Lỗi kết nối khi chuyển đổi tệp!');
        btnElement.disabled = false;
        btnElement.innerHTML = originalContent;
    }
}

async function indexSingleFile(filename, btnElement) {
    if (!confirm(`Bạn có chắc chắn muốn Index file ${filename}?`)) return;
    const originalText = btnElement.innerHTML;
    btnElement.disabled = true;
    btnElement.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang Index...';
    const actionStatus = document.getElementById('action-status');
    if (actionStatus) {
        actionStatus.className = 'status-msg';
        actionStatus.style.display = 'block';
        actionStatus.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Đang Index file ${filename}...`;
    }
    try {
        const res = await adminFetch('/api/admin/index/selected', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ files: [filename] })
        });
        const data = await res.json();
        if (res.ok && data.status === 'success') {
            btnElement.innerHTML = '<i class="fa-solid fa-check"></i> Indexed';
            btnElement.classList.replace('primary', 'secondary');
            if (actionStatus) {
                actionStatus.className = 'status-msg';
                actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(data.message)}`;
            }
            alert(`Index thành công file ${filename}`);
            setTimeout(() => loadAdminData(), 1500);
        } else {
            if (actionStatus) {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.message)}`;
            }
            alert(`Lỗi khi Index file ${filename}: ${data.message || 'Không xác định'}`);
            btnElement.disabled = false;
            btnElement.innerHTML = originalText;
        }
    } catch (e) {
        if (actionStatus) {
            actionStatus.className = 'status-msg error';
            actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Lỗi kết nối`;
        }
        alert(`Lỗi kết nối khi Index file ${filename}`);
        btnElement.disabled = false;
        btnElement.innerHTML = originalText;
    }
}

async function deleteSingleFile(filename, btnElement) {
    if (!confirm(`Bạn có chắc chắn muốn xóa vĩnh viễn tệp ${filename}? Hành động này không thể hoàn tác.`)) return;
    
    const originalText = btnElement.innerHTML;
    btnElement.disabled = true;
    btnElement.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Xóa...';
    
    try {
        const res = await adminFetch(`/api/admin/files/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });
        const data = await res.json();
        
        if (data.status === 'success') {
            alert(`Đã xóa: ${data.message}`);
            loadAdminData();
        } else {
            alert(`Lỗi: ${data.message}`);
            btnElement.disabled = false;
            btnElement.innerHTML = originalText;
        }
    } catch (e) {
        alert('Lỗi kết nối khi xóa tệp!');
        btnElement.disabled = false;
        btnElement.innerHTML = originalText;
    }
}
