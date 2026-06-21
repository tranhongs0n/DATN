export async function streamChatResponse(message, history, contentNode, chatBox) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, history })
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
                        if (assistantMessageText.includes('searching-dots')) {
                            contentNode.innerHTML = assistantMessageText;
                        } else {
                            contentNode.innerHTML = DOMPurify.sanitize(marked.parse(assistantMessageText));
                        }
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                } catch(e) {}
            }
        }
    }
    return assistantMessageText;
}
