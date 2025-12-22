/**
 * Crystal Agent - Magazine Style Frontend
 * Clean, minimalist implementation with Optimistic UI
 */

// ==================== Configuration ====================
const API_BASE_URL = 'http://localhost:8000';

// Debouncing flag
let isSendingMessage = false;

// ==================== Initialization ====================
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔮 Crystal Agent - Magazine Style initialized');

    // Configure marked.js
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            breaks: true,
            gfm: true
        });
    }

    setupEventListeners();
    checkBackendConnection();
});

// ==================== Event Listeners ====================
function setupEventListeners() {
    const messageInput = document.getElementById('user-input');

    // Send on Enter key (without Shift)
    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-resize textarea
        messageInput.addEventListener('input', () => {
            messageInput.style.height = 'auto';
            messageInput.style.height = messageInput.scrollHeight + 'px';
        });
    }
}

// ==================== Message Functions ====================

/**
 * Send message to backend with Optimistic UI
 */
async function sendMessage() {
    // Debouncing: Prevent rapid-fire clicks
    if (isSendingMessage) {
        console.log('⚠️ Message already sending...');
        return;
    }

    const messageInput = document.getElementById('user-input');
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Set debouncing flag
    isSendingMessage = true;

    // ========== OPTIMISTIC UI: Instant User Feedback ==========
    // Step 1: Show user message immediately
    addUserMessage(message);

    // Step 2: Clear input and refocus
    messageInput.value = '';
    messageInput.style.height = 'auto';
    messageInput.focus();

    // Step 3: Scroll to bottom
    scrollToBottom();

    try {
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Show agent response
        if (data.response) {
            addAgentMessage(data.response);
        } else {
            addAgentMessage('エラーが発生しました。もう一度お試しください。');
        }

    } catch (error) {
        console.error('Error sending message:', error);
        addAgentMessage('申し訳ございません。接続エラーが発生しました。');
    } finally {
        // Reset debouncing flag
        isSendingMessage = false;
    }
}

/**
 * Add user message to chat (instant, no network delay)
 */
function addUserMessage(text) {
    const chatContainer = document.getElementById('chat-container');
    if (!chatContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = '👤';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const nameDiv = document.createElement('div');
    nameDiv.className = 'message-name';
    nameDiv.textContent = 'You';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;

    contentDiv.appendChild(nameDiv);
    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}

/**
 * Add agent message to chat with markdown rendering
 */
function addAgentMessage(text) {
    const chatContainer = document.getElementById('chat-container');
    if (!chatContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent';

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = '🔮';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const nameDiv = document.createElement('div');
    nameDiv.className = 'message-name';
    nameDiv.textContent = 'Crystal';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';

    // Render markdown
    if (typeof marked !== 'undefined') {
        textDiv.innerHTML = marked.parse(text);
    } else {
        textDiv.textContent = text;
    }

    contentDiv.appendChild(nameDiv);
    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
}

/**
 * Scroll chat to bottom smoothly
 */
function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        setTimeout(() => {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }
}

// ==================== Backend Connection ====================

/**
 * Check if backend is accessible
 */
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
        });

        if (response.ok) {
            console.log('✅ Backend connected');
        } else {
            console.warn('⚠️ Backend connection issue');
        }
    } catch (error) {
        console.error('❌ Backend not accessible:', error);
    }
}

// ==================== Console Ready Message ====================
console.log('Features: Magazine Style | Optimistic UI | Markdown | Zero Latency');
