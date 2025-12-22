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
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');

    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            sendMessage();
        });
    }

    // Optional: Send on Enter key
    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
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

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Set debouncing flag
    isSendingMessage = true;

    // Disable send button
    if (sendButton) {
        sendButton.disabled = true;
    }

    // ========== OPTIMISTIC UI: Instant User Feedback ==========
    // Step 1: Show user message immediately
    addUserMessage(message);

    // Step 2: Clear input and refocus
    messageInput.value = '';
    messageInput.focus();

    // Step 3: Scroll to bottom
    scrollToBottom();

    // ========== BACKGROUND: Network Request ==========
    // Step 4: Show typing indicator
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

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();

        // Show agent response
        if (data.response) {
            addAgentMessage(data.response);
        } else {
            addAgentMessage('エラーが発生しました。もう一度お試しください。');
        }

    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addAgentMessage('申し訳ございません。接続エラーが発生しました。');
    } finally {
        // Re-enable send button
        if (sendButton) {
            sendButton.disabled = false;
        }
        // Reset debouncing flag
        isSendingMessage = false;
    }
}

/**
 * Add user message to chat (instant, no network delay)
 */
function addUserMessage(text) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message message-enter';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;

    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    scrollToBottom();
}

/**
 * Add agent message to chat with markdown rendering
 */
function addAgentMessage(text) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent-message message-enter';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';

    // Render markdown
    if (typeof marked !== 'undefined') {
        textDiv.innerHTML = marked.parse(text);
    } else {
        textDiv.textContent = text;
    }

    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

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
 * Scroll chat to bottom smoothly
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
