import { addMessage } from './ui.js';
import { streamChatResponse } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    let chatHistory = [];
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            addMessage('user', message);
            chatInput.value = '';
            
            const contentNode = addMessage('assistant', '');
            contentNode.innerHTML = `
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>`;

            try {
                const assistantMessageText = await streamChatResponse(message, chatHistory, contentNode, chatBox);
                chatHistory.push({ role: "user", content: message });
                chatHistory.push({ role: "assistant", content: assistantMessageText });
            } catch (error) {
                contentNode.innerHTML = `<span style="color:var(--error)">Connection error: ${error.message}</span>`;
            }
        });
    }
});
