(function() {
    // Configuration
    const scriptTag = document.currentScript;
    const apiBase = scriptTag.getAttribute('data-api') || window.location.origin;
    
    // Create Shadow Host
    const container = document.createElement('div');
    container.id = 'tlu-chat-widget';
    document.body.appendChild(container);
    const shadow = container.attachShadow({ mode: 'open' });

    // Inject Styles
    const styleLink = document.createElement('link');
    styleLink.rel = 'stylesheet';
    styleLink.href = `${apiBase}/css/bubble.css`;
    shadow.appendChild(styleLink);

    // Font Awesome for Icons
    const faLink = document.createElement('link');
    faLink.rel = 'stylesheet';
    faLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
    shadow.appendChild(faLink);

    // Main HTML Structure
    const widgetHTML = `
        <div class="bubble-container" id="bubble-trigger">
            <div class="bubble-ring"></div>
            <div class="bubble-orb">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </div>
        </div>

        <div class="chat-window" id="chat-window">
            <div class="chat-header">
                <div class="header-info">
                    <div class="status-dot"></div>
                    <span class="header-title">TLU Admissions Assistant</span>
                </div>
                <div class="close-btn" id="close-chat">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
            </div>
            
            <div class="chat-messages" id="messages-container">
                <div class="message assistant">
                    Xin chào! Tôi có thể giúp gì cho bạn về thông tin tuyển sinh Đại học Thủy Lợi?
                </div>
            </div>

            <div class="chat-input-area">
                <form id="widget-chat-form">
                    <div class="input-wrapper">
                        <input type="text" id="widget-input" placeholder="Hỏi về mã ngành, điểm chuẩn..." autocomplete="off">
                        <button type="submit" class="send-btn" id="widget-send-btn">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;

    const widgetDiv = document.createElement('div');
    widgetDiv.innerHTML = widgetHTML;
    shadow.appendChild(widgetDiv);

    // State
    let history = [];
    let isOpen = false;

    // Elements
    const bubbleTrigger = shadow.getElementById('bubble-trigger');
    const chatWindow = shadow.getElementById('chat-window');
    const closeChat = shadow.getElementById('close-chat');
    const chatForm = shadow.getElementById('widget-chat-form');
    const chatInput = shadow.getElementById('widget-input');
    const messagesContainer = shadow.getElementById('messages-container');
    const sendBtn = shadow.getElementById('widget-send-btn');

    // Toggle Chat
    bubbleTrigger.addEventListener('click', () => {
        isOpen = !isOpen;
        chatWindow.classList.toggle('active', isOpen);
    });

    closeChat.addEventListener('click', (e) => {
        e.stopPropagation();
        isOpen = false;
        chatWindow.classList.remove('active');
    });

    // Chat Logic
    function addMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        msgDiv.textContent = text;
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return msgDiv;
    }

    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return typingDiv;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        chatInput.value = '';
        chatInput.disabled = true;
        sendBtn.disabled = true;

        addMessage('user', text);
        const typing = showTyping();

        try {
            const response = await fetch(`${apiBase}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, history: history })
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullText = '';
            
            // Remove typing indicator when first chunk arrives
            let typingRemoved = false;
            const assistantMsgDiv = document.createElement('div');
            assistantMsgDiv.className = 'message assistant';
            messagesContainer.appendChild(assistantMsgDiv);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                if (!typingRemoved) {
                    typing.remove();
                    typingRemoved = true;
                }

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.slice(6);
                        if (dataStr.trim() === '[DONE]') continue;
                        try {
                            const data = JSON.parse(dataStr);
                            if (data.text) {
                                fullText = data.text;
                                assistantMsgDiv.innerHTML = fullText;
                                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                            }
                        } catch (e) {}
                    }
                }
            }

            history.push({ role: 'user', content: text });
            history.push({ role: 'assistant', content: fullText });

        } catch (error) {
            typing.remove();
            addMessage('assistant', 'Xin lỗi, có lỗi kết nối xảy ra. Vui lòng thử lại sau.');
            console.error('Chat Widget Error:', error);
        } finally {
            chatInput.disabled = false;
            sendBtn.disabled = false;
            chatInput.focus();
        }
    });

})();
