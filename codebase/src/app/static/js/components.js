class AppSidebar extends HTMLElement {
    connectedCallback() {
        const currentPath = window.location.pathname;
        const isChat = currentPath === '/' || currentPath === '/index.html';
        const isAdmin = currentPath.startsWith('/admin');
        
        this.innerHTML = `
        <nav class="sidebar">
            <div class="logo" title="TLU RAG">
                <i class="fa-solid fa-graduation-cap"></i>
                <span>TLU RAG</span>
            </div>
            <ul class="nav-links">
                <li class="${isChat ? 'active' : ''}"><a href="/" title="Chat" class="w-100"><i class="fa-regular fa-comment-dots"></i> <span>Chat</span></a></li>
                <li class="${isAdmin ? 'active' : ''}"><a href="/admin" title="Quản trị" class="w-100"><i class="fa-solid fa-gear"></i> <span>Quản trị</span></a></li>
            </ul>
        </nav>
        `;
    }
}

customElements.define('app-sidebar', AppSidebar);
