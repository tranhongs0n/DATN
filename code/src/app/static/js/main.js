document.addEventListener('DOMContentLoaded', () => {
    // Auth State
    let authToken = localStorage.getItem('authToken');

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

    // Auth Elements
    const loginModal = document.getElementById('login-modal');
    const loginForm = document.getElementById('login-form');
    const loginUsername = document.getElementById('login-username');
    const loginPassword = document.getElementById('login-password');
    const loginError = document.getElementById('login-error');
    const logoutBtn = document.getElementById('logout-btn');

    // User Elements
    const usersTableBody = document.querySelector('#users-table tbody');
    const createUserForm = document.getElementById('create-user-form');
    const newUsername = document.getElementById('new-username');
    const newPassword = document.getElementById('new-password');
    const userStatus = document.getElementById('user-status');

    // Zalo Elements
    const conversationList = document.getElementById('conversation-list');
    const zaloChatBox = document.getElementById('zalo-chat-box');
    const currentZaloUser = document.getElementById('current-zalo-user');
    const zaloReplyForm = document.getElementById('zalo-reply-form');
    const zaloReplyInput = document.getElementById('zalo-reply-input');
    const zaloReplyBtn = document.getElementById('zalo-reply-btn');
    const blockUserBtn = document.getElementById('block-user-btn');
    const blockedTableBody = document.querySelector('#blocked-table tbody');
    let selectedZaloUserId = null;

    // Authenticated Fetch wrapper
    async function adminFetch(url, options = {}) {
        if (!options.headers) options.headers = {};
        if (authToken) options.headers['Authorization'] = 'Bearer ' + authToken;
        
        const res = await fetch(url, options);
        if (res.status === 401) {
            authToken = null;
            localStorage.removeItem('authToken');
            loginModal.classList.add('active');
            throw new Error('Unauthorized');
        }
        return res;
    }

    // Login logic
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
                authToken = data.token;
                localStorage.setItem('authToken', authToken);
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

    logoutBtn.addEventListener('click', async () => {
        if (authToken) {
            try {
                await adminFetch('/api/auth/logout', { method: 'POST' });
            } catch (e) {}
            authToken = null;
            localStorage.removeItem('authToken');
        }
        loginModal.classList.add('active');
        // Switch back to chat view visually
        navItems[0].click();
    });

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
                if (!authToken) {
                    loginModal.classList.add('active');
                } else {
                    loginModal.classList.remove('active');
                    loadAdminData();
                }
            } else {
                loginModal.classList.remove('active');
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
            const [statsRes, filesRes, unsupportedRes, usersRes, convsRes, blockedRes] = await Promise.all([
                adminFetch('/api/admin/stats'),
                adminFetch('/api/admin/files'),
                adminFetch('/api/admin/files/unsupported'),
                adminFetch('/api/admin/users'),
                adminFetch('/api/admin/conversations'),
                adminFetch('/api/admin/conversations/blocked')
            ]);
            
            const stats = await statsRes.json();
            const files = await filesRes.json();
            const unsupported = await unsupportedRes.json();
            const users = await usersRes.json();
            const convs = await convsRes.json();
            const blockedData = await blockedRes.json();

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

            // Render users
            usersTableBody.innerHTML = users.users.map(u => `
                <tr>
                    <td>${u.id}</td>
                    <td>${u.username}</td>
                    <td><span class="badge" style="background:var(--primary);color:white;">${u.role}</span></td>
                    <td>
                        <button class="btn delete-user-btn" data-id="${u.id}" style="background: var(--error); color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer;">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');

            // Render Zalo Conversations
            conversationList.innerHTML = convs.conversations.map(c => `
                <div class="conv-item" data-id="${c.user_id}" style="padding: 1rem; border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.2s; background: ${selectedZaloUserId === c.user_id ? 'var(--border)' : 'transparent'};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>User: ${c.user_id.substring(0, 15)}...</strong>
                        ${c.needs_human ? '<span class="badge error" style="background: var(--error); color: white; font-size: 0.6rem; padding: 2px 4px; border-radius: 4px;">Human Needed</span>' : ''}
                    </div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem;">${new Date(c.last_activity * 1000).toLocaleString()}</div>
                </div>
            `).join('');

            // Render Blocked Users
            if (blockedData.status === 'success') {
                blockedTableBody.innerHTML = blockedData.blocked_users.map(b => `
                    <tr>
                        <td>${b.user_id}</td>
                        <td>${new Date(b.blocked_at * 1000).toLocaleString()}</td>
                        <td>${escapeHtml(b.reason || 'N/A')}</td>
                        <td>
                            <button class="btn unblock-btn" data-id="${b.user_id}" style="background: var(--success); color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer;">
                                <i class="fa-solid fa-unlock"></i> Unblock
                            </button>
                        </td>
                    </tr>
                `).join('');
            }

            // Add Zalo Conversation click listeners
            document.querySelectorAll('.conv-item').forEach(item => {
                item.addEventListener('click', () => {
                    document.querySelectorAll('.conv-item').forEach(i => i.style.background = 'transparent');
                    item.style.background = 'var(--border)';
                    loadZaloHistory(item.getAttribute('data-id'));
                });
            });

            // Add conversion event listeners
            document.querySelectorAll('.convert-btn').forEach(btn => {
                btn.addEventListener('click', () => convertFile(btn.getAttribute('data-file'), btn));
            });

            // Add delete user listeners
            document.querySelectorAll('.delete-user-btn').forEach(btn => {
                btn.addEventListener('click', async () => {
                    if (confirm('Are you sure you want to delete this user?')) {
                        try {
                            const res = await adminFetch(`/api/admin/users/${btn.getAttribute('data-id')}`, { method: 'DELETE' });
                            const data = await res.json();
                            if(data.status === 'success') loadAdminData();
                            else alert(data.detail || 'Error');
                        } catch (e) {}
                    }
                });
            });

            // Add unblock user listeners
            document.querySelectorAll('.unblock-btn').forEach(btn => {
                btn.addEventListener('click', async () => {
                    if (confirm('Are you sure you want to unblock this user?')) {
                        try {
                            const res = await adminFetch(`/api/admin/conversations/${btn.getAttribute('data-id')}/unblock`, { method: 'POST' });
                            const data = await res.json();
                            if(data.status === 'success') loadAdminData();
                            else alert(data.message || 'Error');
                        } catch (e) {}
                    }
                });
            });

        } catch (error) {
            console.error('Error loading admin data', error);
        }
    }

    // Zalo specific logic
    async function loadZaloHistory(userId) {
        selectedZaloUserId = userId;
        currentZaloUser.textContent = `Chat with User: ${userId.substring(0, 15)}...`;
        blockUserBtn.style.display = 'inline-block';
        zaloReplyInput.disabled = false;
        zaloReplyBtn.disabled = false;
        zaloChatBox.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Loading...';

        try {
            const res = await adminFetch(`/api/admin/conversations/${userId}`);
            const data = await res.json();
            
            zaloChatBox.innerHTML = '';
            data.history.forEach(msg => {
                const msgDiv = document.createElement('div');
                // msg.role is 'user' or 'assistant'/'admin'
                const isUser = msg.role === 'user';
                msgDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
                
                let avatarIcon = isUser ? '<i class="fa-solid fa-user"></i>' : (msg.role === 'admin' ? '<i class="fa-solid fa-user-shield"></i>' : '<i class="fa-solid fa-robot"></i>');
                
                msgDiv.innerHTML = `
                    <div class="avatar">${avatarIcon}</div>
                    <div class="content" style="background: ${msg.role === 'admin' ? '#1c3d5a' : ''}">${escapeHtml(msg.content)}</div>
                `;
                zaloChatBox.appendChild(msgDiv);
            });
            zaloChatBox.scrollTop = zaloChatBox.scrollHeight;
        } catch (err) {
            zaloChatBox.innerHTML = 'Error loading history.';
        }
    }

    blockUserBtn.addEventListener('click', async () => {
        if (!selectedZaloUserId) return;
        const reason = prompt("Enter a reason for blocking this user (optional):", "Spam");
        if (reason !== null) {
            try {
                const res = await adminFetch(`/api/admin/conversations/${selectedZaloUserId}/block`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reason })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert('User blocked successfully.');
                    blockUserBtn.style.display = 'none';
                    loadAdminData(); // Refresh to show in Blocked table
                } else {
                    alert('Failed to block user: ' + data.message);
                }
            } catch (err) {
                alert('Connection error.');
            }
        }
    });

    zaloReplyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!selectedZaloUserId) return;
        
        const message = zaloReplyInput.value.trim();
        if (!message) return;

        zaloReplyInput.disabled = true;
        zaloReplyBtn.disabled = true;

        try {
            const res = await adminFetch(`/api/admin/conversations/${selectedZaloUserId}/reply`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            if (res.ok) {
                zaloReplyInput.value = '';
                loadZaloHistory(selectedZaloUserId);
            } else {
                alert('Failed to send message.');
            }
        } catch (err) {
            alert('Connection error.');
        } finally {
            zaloReplyInput.disabled = false;
            zaloReplyBtn.disabled = false;
            zaloReplyInput.focus();
        }
    });

    createUserForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        userStatus.className = 'status-msg';
        userStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Creating user...';
        
        try {
            const res = await adminFetch('/api/admin/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: newUsername.value, password: newPassword.value })
            });
            const data = await res.json();
            
            if (res.ok && data.status === 'success') {
                userStatus.innerHTML = '<i class="fa-solid fa-check"></i> User created!';
                createUserForm.reset();
                loadAdminData();
            } else {
                userStatus.className = 'status-msg error';
                userStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.detail || 'Error'}`;
            }
        } catch (err) {
            userStatus.className = 'status-msg error';
            userStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Connection error`;
        }
    });

    rebuildBtn.addEventListener('click', async () => {
        actionStatus.className = 'status-msg';
        actionStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Rebuilding index...';
        
        try {
            const res = await adminFetch('/api/admin/index/rebuild', { method: 'POST' });
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
            const res = await adminFetch('/api/admin/index/upload', {
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
            const res = await adminFetch('/api/admin/files/convert', {
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
        const scrapeLimitInput = document.getElementById('scrape-limit');
        const limitVal = scrapeLimitInput ? parseInt(scrapeLimitInput.value) : 5;

        scrapeStatus.className = 'status-msg';
        scrapeStatus.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Scraping TLU portal (this may take a while)...';
        scrapeBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('category', 'all');
            formData.append('limit', limitVal);

            const res = await adminFetch('/api/admin/scrape', {
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
            const res = await adminFetch('/api/admin/files/convert-all', { method: 'POST' });
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
