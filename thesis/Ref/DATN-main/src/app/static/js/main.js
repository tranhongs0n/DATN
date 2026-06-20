document.addEventListener('DOMContentLoaded', () => {
    // State
    let chatHistory = [];
    
    // DOM Elements
    const navItems = document.querySelectorAll('.nav-links li');
    const views = document.querySelectorAll('.view');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');
    
    const rebuildBtn = document.getElementById('rebuild-btn');
    const fileUpload = document.getElementById('file-upload');
    const actionStatus = document.getElementById('action-status');
    const statsContent = document.getElementById('stats-content');
    const filesTableBody = document.querySelector('#files-table tbody');
    const unsupportedTableBody = document.querySelector('#unsupported-table tbody');
    
    const scrapeBtn = document.getElementById('scrape-btn');
    const scrapeStatus = document.getElementById('scrape-status');
    const bulkConvertBtn = document.getElementById('bulk-convert-btn');

    // Navigation
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            
            const viewId = item.getAttribute('data-view') + '-view';
            views.forEach(v => {
                if(v.id === viewId) v.classList.add('active');
                else v.classList.remove('active');
            });

            if(viewId === 'admin-view') {
                loadAdminData();
            }
        });
    });

    // Chat functionality
    function addMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'content';
        content.innerHTML = role === 'user' ? escapeHtml(text) : marked.parse(text || '');
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatBox.appendChild(msgDiv);
        
        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
        
        return content;
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage('user', message);
        chatInput.value = '';
        
        // Add empty assistant message
        const contentNode = addMessage('assistant', '');
        contentNode.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>`;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, history: chatHistory })
            });

            if (!response.ok) throw new Error('API Error');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let assistantMessageText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.slice(6);
                        if(dataStr.trim() === '[DONE]') continue;
                        
                        try {
                            const data = JSON.parse(dataStr);
                            if (data.error) {
                                contentNode.innerHTML = `<span style="color:var(--error)">Error: ${data.error}</span>`;
                            } else if (data.text) {
                                assistantMessageText = data.text;
                                // If it's the status message, don't use marked to avoid escaping/wrapping issues
                                if (assistantMessageText.includes('searching-dots')) {
                                    contentNode.innerHTML = assistantMessageText;
                                } else {
                                    contentNode.innerHTML = marked.parse(assistantMessageText);
                                }
                                chatBox.scrollTop = chatBox.scrollHeight;
                            }
                        } catch(e) {
                            console.error("JSON parse error for line:", line);
                        }
                    }
                }
            }

            // Update history
            chatHistory.push({ role: "user", content: message });
            chatHistory.push({ role: "assistant", content: assistantMessageText });

        } catch (error) {
            contentNode.innerHTML = `<span style="color:var(--error)">Connection error: ${error.message}</span>`;
        }
    });

    // Admin functionality
    async function loadAdminData() {
        try {
            const [statsRes, filesRes, unsupportedRes] = await Promise.all([
                fetch('/api/admin/stats'),
                fetch('/api/admin/files'),
                fetch('/api/admin/files/unsupported')
            ]);
            
            const stats = await statsRes.json();
            const files = await filesRes.json();
            const unsupported = await unsupportedRes.json();

            // Render stats
            statsContent.innerHTML = `
                <ul style="list-style:none; line-height: 2;">
                    <li><strong>Documents:</strong> ${stats.doc_count}</li>
                    <li><strong>Chunks:</strong> ${stats.chunk_count}</li>
                    <li><strong>Embedding Model:</strong> <code>${stats.embedding_model}</code></li>
                    <li><strong>LLM Model:</strong> <code>${stats.llm_model}</code></li>
                </ul>
            `;

            // Render files
            filesTableBody.innerHTML = files.files.map(f => `
                <tr>
                    <td>${f.name}</td>
                    <td><span style="color: ${f.status.includes('Indexed') ? 'var(--success)' : 'var(--warning)'}">${f.status}</span></td>
                    <td style="font-size: 0.85em; color: var(--text-secondary);">${f.path}</td>
                </tr>
            `).join('');

            // Render unsupported
            unsupportedTableBody.innerHTML = unsupported.files.map(f => `
                <tr>
                    <td>${f.name}</td>
                    <td><span class="badge unsupported">${f.extension}</span></td>
                    <td>
                        <button class="btn primary small convert-btn" data-file="${f.name}">
                            <i class="fa-solid fa-wand-sparkles"></i> Convert
                        </button>
                    </td>
                </tr>
            `).join('');

            // Add conversion event listeners
            document.querySelectorAll('.convert-btn').forEach(btn => {
                btn.addEventListener('click', () => convertFile(btn.getAttribute('data-file'), btn));
            });

        } catch (error) {
            console.error('Error loading admin data', error);
        }
    }

    rebuildBtn.addEventListener('click', async () => {
        actionStatus.className = 'status-msg';
        actionStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Rebuilding index...';
        
        try {
            const res = await fetch('/api/admin/index/rebuild', { method: 'POST' });
            const data = await res.json();
            
            if (data.status === 'success') {
                actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${data.message}`;
                loadAdminData();
            } else {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.message}`;
            }
        } catch (e) {
            actionStatus.className = 'status-msg error';
            actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Error rebuilding index`;
        }
    });

    fileUpload.addEventListener('change', async (e) => {
        const files = e.target.files;
        if (!files.length) return;

        const formData = new FormData();
        for (const file of files) {
            formData.append('files', file);
        }

        actionStatus.className = 'status-msg';
        actionStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Uploading & indexing...';
        
        try {
            const res = await fetch('/api/admin/index/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            
            if (data.status === 'success') {
                actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${data.message}`;
                loadAdminData();
            } else {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.message}`;
            }
        } catch (err) {
            actionStatus.className = 'status-msg error';
            actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Upload failed`;
        }
    });

    async function convertFile(filename, btnElement) {
        const originalContent = btnElement.innerHTML;
        btnElement.disabled = true;
        btnElement.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Converting...';
        
        try {
            const res = await fetch('/api/admin/files/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename })
            });
            const data = await res.json();
            
            if (data.status === 'success') {
                actionStatus.className = 'status-msg';
                actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${data.message}`;
                loadAdminData();
            } else {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.message}`;
                btnElement.disabled = false;
                btnElement.innerHTML = originalContent;
            }
        } catch (err) {
            actionStatus.className = 'status-msg error';
            actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Conversion failed`;
            btnElement.disabled = false;
            btnElement.innerHTML = originalContent;
        }
    }

    scrapeBtn.addEventListener('click', async () => {
        scrapeStatus.className = 'status-msg';
        scrapeStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Scraping TLU portal (this may take a while)...';
        scrapeBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('category', 'all');
            formData.append('limit', 5); // Limit per category for safety

            const res = await fetch('/api/admin/scrape', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            if (data.status === 'success') {
                scrapeStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${data.message}`;
                loadAdminData();
            } else {
                scrapeStatus.className = 'status-msg error';
                scrapeStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.message}`;
            }
        } catch (e) {
            scrapeStatus.className = 'status-msg error';
            scrapeStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Scraping failed`;
        } finally {
            scrapeBtn.disabled = false;
        }
    });

    bulkConvertBtn.addEventListener('click', async () => {
        const originalText = bulkConvertBtn.innerHTML;
        bulkConvertBtn.disabled = true;
        bulkConvertBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing...';
        actionStatus.className = 'status-msg';
        actionStatus.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles fa-bounce"></i> Starting bulk conversion...';

        try {
            const res = await fetch('/api/admin/files/convert-all', { method: 'POST' });
            const data = await res.json();

            if (data.status === 'success' || data.status === 'warning') {
                actionStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${data.message}`;
                loadAdminData();
            } else {
                actionStatus.className = 'status-msg error';
                actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.message}`;
            }
        } catch (e) {
            actionStatus.className = 'status-msg error';
            actionStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Bulk conversion failed`;
        } finally {
            bulkConvertBtn.disabled = false;
            bulkConvertBtn.innerHTML = originalText;
        }
    });
});
