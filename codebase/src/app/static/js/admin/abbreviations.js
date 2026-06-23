import { adminFetch } from './api.js';

export async function loadAbbreviations() {
    const tableBody = document.querySelector('#abbr-table tbody');
    const template = document.getElementById('abbr-row-template');
    
    if (!tableBody || !template) return;
    
    tableBody.innerHTML = '<tr><td colspan="3" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Đang tải dữ liệu...</td></tr>';
    
    try {
        const response = await adminFetch('/api/admin/abbreviations');
        const data = await response.json();
        
        tableBody.innerHTML = '';
        
        if (!data.abbreviations || data.abbreviations.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="3" class="text-center text-secondary">Chưa có từ viết tắt nào</td></tr>';
            return;
        }
        
        data.abbreviations.forEach(abbr => {
            const clone = template.content.cloneNode(true);
            const row = clone.querySelector('tr');
            
            clone.querySelector('.abbr-short').textContent = abbr.short_form;
            clone.querySelector('.abbr-full').textContent = abbr.full_form;
            
            clone.querySelector('.edit-abbr-btn').addEventListener('click', () => {
                showAbbrModal(abbr);
            });
            
            clone.querySelector('.delete-abbr-btn').addEventListener('click', () => {
                if(confirm(`Bạn có chắc chắn muốn xóa từ viết tắt "${abbr.short_form}"?`)) {
                    deleteAbbreviation(abbr.id, row);
                }
            });
            
            tableBody.appendChild(clone);
        });
    } catch (error) {
        tableBody.innerHTML = `<tr><td colspan="3" class="text-center text-error">Lỗi: ${error.message}</td></tr>`;
    }
}

export function setupAbbreviations() {
    const modal = document.getElementById('abbr-modal');
    const form = document.getElementById('abbr-modal-form');
    const addBtn = document.getElementById('add-abbr-btn');
    const cancelBtn = document.getElementById('cancel-abbr-btn');
    const statusMsg = document.getElementById('abbr-status');
    
    if (!modal || !form) return;
    
    addBtn.addEventListener('click', () => {
        document.getElementById('abbr-modal-title').innerHTML = '<i class="fa-solid fa-book"></i> Thêm từ viết tắt mới';
        document.getElementById('abbr-modal-id').value = '';
        form.reset();
        document.getElementById('abbr-modal-error').classList.add('d-none');
        modal.classList.add('active');
    });
    
    cancelBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const id = document.getElementById('abbr-modal-id').value;
        const short_form = document.getElementById('abbr-modal-short').value;
        const full_form = document.getElementById('abbr-modal-full').value;
        const errorDiv = document.getElementById('abbr-modal-error');
        const submitBtn = form.querySelector('button[type="submit"]');
        
        try {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang lưu...';
            errorDiv.classList.add('d-none');
            
            const method = id ? 'PUT' : 'POST';
            const url = id ? `/api/admin/abbreviations/${id}` : '/api/admin/abbreviations';
            
            const response = await adminFetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ short_form, full_form })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                modal.classList.remove('active');
                loadAbbreviations();
            } else {
                throw new Error(data.message || 'Lỗi không xác định');
            }
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('d-none');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Lưu';
        }
    });
    
    const openImportBtn = document.getElementById('open-import-abbr-btn');
    const importModal = document.getElementById('import-abbr-modal');
    const importForm = document.getElementById('import-abbr-form');
    const cancelImportBtn = document.getElementById('cancel-import-abbr-btn');
    const loadSampleBtn = document.getElementById('load-sample-json-btn');
    const jsonTextarea = document.getElementById('import-abbr-json');
    const importError = document.getElementById('import-abbr-error');
    
    if (openImportBtn) {
        openImportBtn.addEventListener('click', () => {
            jsonTextarea.value = '';
            importError.classList.add('d-none');
            importModal.classList.add('active');
        });
    }

    if (cancelImportBtn) {
        cancelImportBtn.addEventListener('click', () => {
            importModal.classList.remove('active');
        });
    }

    if (loadSampleBtn) {
        loadSampleBtn.addEventListener('click', () => {
            const sample = {
                "cntt": "Công nghệ thông tin",
                "httt": "Hệ thống thông tin",
                "ktpm": "Kỹ thuật phần mềm",
                "tmdt": "Thương mại điện tử"
            };
            jsonTextarea.value = JSON.stringify(sample, null, 2);
        });
    }

    if (importForm) {
        importForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = importForm.querySelector('button[type="submit"]');
            
            try {
                // Thử parse JSON trước khi gửi để validate
                let parsedData;
                try {
                    parsedData = JSON.parse(jsonTextarea.value);
                    if (typeof parsedData !== 'object' || Array.isArray(parsedData)) {
                        throw new Error("JSON phải là một Object (Dictionary).");
                    }
                } catch (parseErr) {
                    throw new Error("JSON không hợp lệ: " + parseErr.message);
                }

                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang import...';
                importError.classList.add('d-none');
                
                const response = await adminFetch('/api/admin/abbreviations/import', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(parsedData)
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    importModal.classList.remove('active');
                    statusMsg.className = 'status-msg success';
                    statusMsg.textContent = data.message;
                    loadAbbreviations();
                    setTimeout(() => { statusMsg.className = 'status-msg'; }, 5000);
                } else {
                    throw new Error(data.message || 'Lỗi import');
                }
            } catch (error) {
                importError.textContent = error.message;
                importError.classList.remove('d-none');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Import';
            }
        });
    }
}

function showAbbrModal(abbr) {
    document.getElementById('abbr-modal-title').innerHTML = '<i class="fa-solid fa-pen"></i> Sửa từ viết tắt';
    document.getElementById('abbr-modal-id').value = abbr.id;
    document.getElementById('abbr-modal-short').value = abbr.short_form;
    document.getElementById('abbr-modal-full').value = abbr.full_form;
    document.getElementById('abbr-modal-error').classList.add('d-none');
    document.getElementById('abbr-modal').classList.add('active');
}

async function deleteAbbreviation(id, row) {
    try {
        row.style.opacity = '0.5';
        const response = await adminFetch(`/api/admin/abbreviations/${id}`, { method: 'DELETE' });
        const data = await response.json();
        
        if (data.status === 'success') {
            loadAbbreviations();
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        row.style.opacity = '1';
        alert(`Lỗi xóa: ${error.message}`);
    }
}
