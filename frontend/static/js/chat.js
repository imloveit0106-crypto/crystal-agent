/**
 * Crystal Agent - Streaming Chat Client
 *
 * Features:
 * - Real-time streaming with Server-Sent Events (SSE)
 * - Typewriter effect for AI responses
 * - Markdown rendering with Marked.js
 * - Syntax highlighting with Highlight.js
 * - Smooth auto-scroll
 * - 60fps performance optimization
 */

// ==================== Configuration ====================
const API_BASE_URL = window.location.origin;
const TYPEWRITER_SPEED = 20; // milliseconds per character (50 chars/sec = 60fps smooth)

// ==================== DOM Elements ====================
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const chatForm = document.getElementById('chatForm');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const connectionStatus = document.getElementById('connectionStatus');

// Statistics elements
const statTotalLogs = document.getElementById('statTotalLogs');
const statTasks = document.getElementById('statTasks');
const statSpending = document.getElementById('statSpending');

// Quick action buttons
const quickActionButtons = document.querySelectorAll('.quick-action-btn');

// ==================== State Management ====================
let isStreaming = false;
let currentMessageElement = null;

// ==================== Error Toast Setup ====================
let toastElement = document.getElementById('error-toast');
if (!toastElement) {
    toastElement = document.createElement('div');
    toastElement.id = 'error-toast';
    document.body.appendChild(toastElement);
}

/**
 * Show error toast notification
 */
function showToast(message) {
    toastElement.textContent = message;
    toastElement.className = "show";
    setTimeout(() => {
        toastElement.className = toastElement.className.replace("show", "");
    }, 3000);
}

// ==================== Markdown Configuration ====================
// Configure Marked.js for safe HTML rendering
marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: false,
    mangle: false,
    highlight: function(code, lang) {
        // Syntax highlighting with Highlight.js
        if (lang && hljs.getLanguage(lang)) {
            try {
                return hljs.highlight(code, { language: lang }).value;
            } catch (err) {
                console.error('Highlight error:', err);
            }
        }
        return hljs.highlightAuto(code).value;
    }
});

// ==================== Utility Functions ====================

/**
 * Gentle scroll to bottom of chat
 * Calm Zero-Latency: Small delay for organic, non-aggressive feel
 */
function scrollToBottom(smooth = true, delay = 100) {
    setTimeout(() => {
        requestAnimationFrame(() => {
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: smooth ? 'smooth' : 'auto'
            });
        });
    }, delay);
}

/**
 * Format timestamp
 */
function formatTime() {
    return new Date().toLocaleTimeString('ja-JP', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Render Markdown to HTML
 */
function renderMarkdown(text) {
    return marked.parse(text);
}

// ==================== Message Creation ====================

/**
 * Create user message element with Calm Zero-Latency animation
 */
function createUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message message-enter';
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">You</span>
                <span class="message-badge">${formatTime()}</span>
            </div>
            <div class="message-text">${escapeHtml(text)}</div>
        </div>
    `;
    return messageDiv;
}

/**
 * Create agent message element (empty, to be filled by streaming) with Calm animation
 */
function createAgentMessage(metadata = {}) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent-message message-enter';

    const badge = metadata.detected_type
        ? `<span class="message-badge">${metadata.detected_type}</span>`
        : '';

    messageDiv.innerHTML = `
        <div class="message-avatar">🔮</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">Crystal Agent</span>
                ${badge}
            </div>
            <div class="message-text"></div>
        </div>
    `;
    return messageDiv;
}

// ==================== Streaming & Typewriter Effect ====================

/**
 * Typewriter effect: Append text character by character
 * Optimized for 60fps performance
 */
async function typewriterEffect(element, text, speed = TYPEWRITER_SPEED) {
    let currentText = '';
    const chars = text.split('');

    return new Promise((resolve) => {
        let index = 0;

        function typeNextChar() {
            if (index < chars.length) {
                currentText += chars[index];

                // Render markdown in real-time
                element.innerHTML = renderMarkdown(currentText);

                // Apply syntax highlighting to code blocks
                element.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });

                index++;

                // Smooth scroll as text appears
                scrollToBottom(true);

                // Schedule next character (60fps = ~16ms, but we use custom speed)
                setTimeout(typeNextChar, speed);
            } else {
                resolve();
            }
        }

        typeNextChar();
    });
}

/**
 * Stream chat response using Server-Sent Events (SSE)
 */
async function streamChatResponse(message) {
    if (isStreaming) return;

    isStreaming = true;
    sendButton.disabled = true;
    messageInput.disabled = true;

    // Show typing indicator
    typingIndicator.style.display = 'flex';
    scrollToBottom();

    try {
        // Send message to streaming endpoint
        const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Read the stream using ReadableStream API
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let buffer = '';
        let fullResponse = '';
        let metadata = null;
        let agentMessage = null;

        while (true) {
            const { value, done } = await reader.read();

            if (done) break;

            // Decode chunk
            buffer += decoder.decode(value, { stream: true });

            // Process complete SSE messages (separated by \n\n)
            const lines = buffer.split('\n\n');
            buffer = lines.pop() || ''; // Keep incomplete line in buffer

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));

                    // Handle metadata
                    if (data.type === 'metadata') {
                        metadata = data;

                        // Hide typing indicator and create message
                        typingIndicator.style.display = 'none';
                        agentMessage = createAgentMessage(metadata);
                        chatMessages.appendChild(agentMessage);
                        currentMessageElement = agentMessage.querySelector('.message-text');
                        scrollToBottom();
                        continue;
                    }

                    // Handle errors
                    if (data.error) {
                        console.error('Stream error:', data.error);
                        if (currentMessageElement) {
                            currentMessageElement.innerHTML = `<p style="color: #ff6b6b;">❌ ${data.error}</p>`;
                        }
                        break;
                    }

                    // Handle text chunks
                    if (data.chunk && !data.done) {
                        fullResponse += data.chunk;

                        // Real-time rendering: append chunk with typewriter effect
                        if (currentMessageElement) {
                            // Instant rendering (no delay per chunk, smooth 60fps)
                            currentMessageElement.innerHTML = renderMarkdown(fullResponse);

                            // Apply syntax highlighting
                            currentMessageElement.querySelectorAll('pre code').forEach((block) => {
                                hljs.highlightElement(block);
                            });

                            scrollToBottom(true);
                        }
                    }

                    // Handle completion
                    if (data.done) {
                        // Final render
                        if (currentMessageElement && fullResponse) {
                            currentMessageElement.innerHTML = renderMarkdown(fullResponse);
                            currentMessageElement.querySelectorAll('pre code').forEach((block) => {
                                hljs.highlightElement(block);
                            });
                        }
                        scrollToBottom();
                    }
                }
            }
        }

        // Update statistics after response
        await updateStatistics();

    } catch (error) {
        console.error('Streaming error:', error);

        // Hide typing indicator
        if (typingIndicator.style.display !== 'none') {
            typingIndicator.style.display = 'none';
        }

        // Show error toast (non-intrusive)
        showToast("Unable to reach the agent. Please try again.");

    } finally {
        isStreaming = false;
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
        currentMessageElement = null;
    }
}

// ==================== Statistics ====================

/**
 * Fetch and update statistics
 */
async function updateStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/stats`);
        const stats = await response.json();

        // Animate number changes
        animateValue(statTotalLogs, parseInt(statTotalLogs.textContent) || 0, stats.total_logs || 0, 500);
        animateValue(statTasks, parseInt(statTasks.textContent) || 0, stats.by_type?.['タスク'] || 0, 500);

        const oldSpending = parseInt(statSpending.textContent.replace(/[¥,]/g, '')) || 0;
        const newSpending = stats.total_amount || 0;
        animateValue(
            statSpending,
            oldSpending,
            newSpending,
            500,
            (val) => `¥${Math.round(val).toLocaleString()}`
        );

    } catch (error) {
        console.error('Failed to fetch statistics:', error);
    }
}

/**
 * Animate number changes with easing
 */
function animateValue(element, start, end, duration, formatter = null) {
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function (ease-out-cubic)
        const eased = 1 - Math.pow(1 - progress, 3);

        const current = start + (end - start) * eased;
        element.textContent = formatter ? formatter(current) : Math.round(current);

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// ==================== Event Handlers ====================

/**
 * Handle form submission with Zero Latency UX
 *
 * Optimistic UI approach:
 * 1. INSTANTLY show user's message (before network request)
 * 2. INSTANTLY clear input and restore focus
 * 3. THEN initiate streaming API call
 */
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message || isStreaming) return;

    // ========== IMMEDIATE USER ACTIONS (Zero Latency) ==========

    // Step 1: Append user message INSTANTLY with animation
    const userMessage = createUserMessage(message);
    chatMessages.appendChild(userMessage);

    // Step 2: Clear input and force focus IMMEDIATELY
    messageInput.value = '';
    messageInput.focus();

    // Step 3: Scroll to bottom smoothly
    scrollToBottom(true);

    // ========== BACKGROUND STREAMING (Network) ==========

    // Step 4: Initiate API request (SSE streaming)
    await streamChatResponse(message);
});

/**
 * Handle quick action buttons
 */
quickActionButtons.forEach(button => {
    button.addEventListener('click', () => {
        const action = button.getAttribute('data-action');
        messageInput.value = action;
        messageInput.focus();
    });
});

/**
 * Auto-focus input on page load
 */
window.addEventListener('load', () => {
    messageInput.focus();
    updateStatistics();
});

/**
 * Handle Enter key (Shift+Enter for new line)
 */
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// ==================== Connection Status ====================

/**
 * Check server health
 */
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        const indicator = connectionStatus.querySelector('.status-indicator');
        const text = connectionStatus.querySelector('.status-text');

        if (data.status === 'healthy') {
            indicator.style.background = '#10b981';
            text.textContent = data.ai_configured ? 'Connected' : 'Demo Mode';
        } else {
            indicator.style.background = '#f59e0b';
            text.textContent = 'Reconnecting...';
        }
    } catch (error) {
        const indicator = connectionStatus.querySelector('.status-indicator');
        const text = connectionStatus.querySelector('.status-text');
        indicator.style.background = '#ef4444';
        text.textContent = 'Disconnected';
    }
}

// Check health on load and every 30 seconds
checkHealth();
setInterval(checkHealth, 30000);

// ==================== Performance Monitoring ====================

// Log FPS in development
if (window.location.hostname === 'localhost') {
    let lastTime = performance.now();
    let frames = 0;

    function measureFPS() {
        frames++;
        const currentTime = performance.now();

        if (currentTime >= lastTime + 1000) {
            const fps = Math.round((frames * 1000) / (currentTime - lastTime));
            console.log(`FPS: ${fps}`);
            frames = 0;
            lastTime = currentTime;
        }

        requestAnimationFrame(measureFPS);
    }

    // measureFPS(); // Uncomment to enable FPS monitoring
}

console.log('🔮 Crystal Agent Streaming Chat - Ready');
console.log('Features: SSE Streaming | Zero Latency UX | Markdown | Syntax Highlighting | 60fps');
console.log('✨ Optimistic UI: Instant user feedback with real-time AI streaming');
