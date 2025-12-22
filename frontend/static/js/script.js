/**
 * Crystal Agent - Frontend JavaScript
 * Purple Glassmorphism Theme with Full Backend Integration
 */

// ==================== Configuration ====================
const API_BASE_URL = 'http://localhost:8000';

// Debouncing flag
let isSendingMessage = false;

// ==================== Initialization ====================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🔮 Crystal Agent initialized');

    // Initialize marked.js options
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            breaks: true,
            gfm: true
        });
    }

    // Initialize Lucide icons if available
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    await loadStats();
    await checkConnection();
    setupEventListeners();
    checkFirstVisit();
});

// ==================== Event Listeners ====================
function setupEventListeners() {
    // Chat form submission
    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            sendMessage();
        });
    }

    // Quick action buttons
    const quickActionBtns = document.querySelectorAll('.quick-action-btn');
    quickActionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.getAttribute('data-action');
            const messageInput = document.getElementById('messageInput');
            if (messageInput) {
                messageInput.value = action;
                messageInput.focus();
            }
        });
    });

    // Help modal
    const helpButton = document.getElementById('helpButton');
    const helpModal = document.getElementById('helpModal');
    const helpModalClose = document.getElementById('helpModalClose');
    const helpModalOverlay = helpModal?.querySelector('.help-modal-overlay');

    if (helpButton && helpModal) {
        helpButton.addEventListener('click', () => {
            helpModal.classList.add('active');
        });
    }

    if (helpModalClose && helpModal) {
        helpModalClose.addEventListener('click', () => {
            helpModal.classList.remove('active');
        });
    }

    if (helpModalOverlay && helpModal) {
        helpModalOverlay.addEventListener('click', () => {
            helpModal.classList.remove('active');
        });
    }

    // ESC key to close modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && helpModal?.classList.contains('active')) {
            helpModal.classList.remove('active');
        }
    });
}

// ==================== Help Modal Functions ====================
function checkFirstVisit() {
    const hasVisited = localStorage.getItem('crystal_agent_visited');
    if (!hasVisited) {
        setTimeout(() => {
            const helpModal = document.getElementById('helpModal');
            if (helpModal) {
                helpModal.classList.add('active');
            }
        }, 1000);
        localStorage.setItem('crystal_agent_visited', 'true');
    }
}

// ==================== Message Functions ====================

/**
 * Send message to backend
 */
async function sendMessage() {
    // Debouncing
    if (isSendingMessage) {
        console.log('⚠️ 送信処理中です。しばらくお待ちください。');
        return;
    }

    const input = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const message = input.value.trim();

    if (!message) {
        return;
    }

    // Set debouncing flag
    isSendingMessage = true;

    // Disable send button
    if (sendButton) {
        sendButton.disabled = true;
        sendButton.style.opacity = '0.7';
    }

    // Add user message
    addUserMessage(message);
    input.value = '';
    input.focus();

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();

        // Add agent message
        if (data.response) {
            addAgentMessage(data.response, data);
        }

    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addAgentMessage('申し訳ございません。エラーが発生しました。もう一度お試しください。');
    } finally {
        // Re-enable send button
        if (sendButton) {
            sendButton.disabled = false;
            sendButton.style.opacity = '1';
        }
        // Reset debouncing flag
        isSendingMessage = false;
    }
}

/**
 * Add user message to chat
 */
function addUserMessage(text) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message message-enter';

    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">You</span>
            </div>
            <div class="message-text">
                ${escapeHtml(text)}
            </div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add agent message to chat
 */
function addAgentMessage(text, metadata = {}) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent-message message-enter';

    const badge = metadata.detected_type
        ? `<span class="message-badge">${metadata.detected_type}</span>`
        : '<span class="message-badge">AI</span>';

    // Render markdown
    const renderedText = renderMarkdown(text);

    messageDiv.innerHTML = `
        <div class="message-avatar">🔮</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">Crystal Agent</span>
                ${badge}
            </div>
            <div class="message-text">
                ${renderedText}
            </div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);

    // Apply syntax highlighting
    messageDiv.querySelectorAll('pre code').forEach((block) => {
        if (typeof hljs !== 'undefined') {
            hljs.highlightElement(block);
        }
    });

    scrollToBottom();
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.style.display = 'flex';
        scrollToBottom();
    }
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.style.display = 'none';
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        setTimeout(() => {
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }
}

/**
 * Render markdown to HTML
 */
function renderMarkdown(text) {
    if (typeof marked !== 'undefined') {
        return marked.parse(text);
    }
    return escapeHtml(text).replace(/\n/g, '<br>');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== Stats Functions ====================

/**
 * Load statistics from backend
 */
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (response.ok) {
            const stats = await response.json();

            // Update stat cards
            const totalLogsEl = document.getElementById('statTotalLogs');
            const tasksEl = document.getElementById('statTasks');
            const spendingEl = document.getElementById('statSpending');

            if (totalLogsEl) totalLogsEl.textContent = stats.total_logs || 0;
            if (tasksEl) tasksEl.textContent = stats.tasks || 0;
            if (spendingEl) spendingEl.textContent = `¥${stats.total_spending || 0}`;
        }
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

/**
 * Check backend connection
 */
async function checkConnection() {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status-text');

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            if (statusIndicator) {
                statusIndicator.style.backgroundColor = '#10b981';
            }
            if (statusText) {
                statusText.textContent = 'Connected';
            }
        } else {
            throw new Error('Connection failed');
        }
    } catch (error) {
        if (statusIndicator) {
            statusIndicator.style.backgroundColor = '#ef4444';
        }
        if (statusText) {
            statusText.textContent = 'Disconnected';
        }
        console.error('Backend connection failed:', error);
    }
}

// ==================== Console Log ====================
console.log('🔮 Crystal Agent - Ready');
console.log('Features: Purple Glassmorphism | Markdown | Syntax Highlighting | Real-time Stats');
