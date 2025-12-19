/**
 * Crystal Agent - Frontend JavaScript
 * Minimal & Clean Implementation
 */

// ============================================
// Configuration
// ============================================

const API_BASE_URL = 'http://localhost:8000';

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Crystal Agent initialized');
    await loadStats();
    await checkConnection();
    setupEventListeners();
});

// ============================================
// Event Listeners
// ============================================

function setupEventListeners() {
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
}

// ============================================
// Core Functions
// ============================================

/**
 * メッセージ送信
 */
window.sendMessage = async function() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message) {
        input.classList.add('ring-2', 'ring-red-500');
        setTimeout(() => input.classList.remove('ring-2', 'ring-red-500'), 500);
        return;
    }

    addMessage(message, 'user');
    input.value = '';
    showTypingIndicator();

    try {
        const data = await sendChatMessage(message);
        hideTypingIndicator();
        addMessage(data.response, 'assistant', {
            type: data.detected_type,
            amount: data.detected_amount,
            saved: data.saved_to_notion
        });
        await loadStats();
    } catch (error) {
        hideTypingIndicator();
        addMessage('エラーが発生しました。もう一度お試しください。', 'assistant');
        console.error('Send message error:', error);
    }
}

/**
 * クイック入力
 */
window.quickInput = function(text) {
    const input = document.getElementById('messageInput');
    input.value = text;
    input.focus();
}

// ============================================
// API Functions
// ============================================

/**
 * 接続チェック
 */
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        const statusIndicator = document.getElementById('statusIndicator');

        if (data.notion === 'connected' && data.gemini === 'connected') {
            statusIndicator.innerHTML = `
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span class="text-xs font-medium text-gray-600 hidden sm:inline">Online</span>
            `;
        } else {
            statusIndicator.innerHTML = `
                <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span class="text-xs font-medium text-gray-600 hidden sm:inline">Limited</span>
            `;
        }
    } catch (error) {
        console.error('Connection check failed:', error);
        const statusIndicator = document.getElementById('statusIndicator');
        statusIndicator.innerHTML = `
            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
            <span class="text-xs font-medium text-gray-600 hidden sm:inline">Offline</span>
        `;
    }
}

/**
 * 統計データ読み込み
 */
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const stats = await response.json();

        updateNumber('totalCount', stats.total);
        updateNumber('diaryCount', stats.types['日記'] || 0);
        updateNumber('taskCount', stats.types['タスク'] || 0);
    } catch (error) {
        console.error('Stats load failed:', error);
    }
}

/**
 * チャットメッセージ送信
 */
async function sendChatMessage(message) {
    const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, use_rag: true })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

// ============================================
// UI Functions
// ============================================

/**
 * メッセージを追加
 */
function addMessage(text, role, meta = {}) {
    const container = document.getElementById('chatContainer').querySelector('.max-w-3xl');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-fade-in';

    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="flex justify-end items-start gap-3">
                <div class="bg-gray-900 text-white rounded-xl px-5 py-3.5 max-w-[75%]">
                    <p class="text-base leading-relaxed">${escapeHtml(text)}</p>
                </div>
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                    <i data-lucide="user" class="w-4 h-4 text-gray-400"></i>
                </div>
            </div>
        `;
    } else {
        const metaInfo = meta.saved ? `
            <div class="flex gap-2 mt-2">
                <span class="text-xs px-2.5 py-1 bg-gray-100 text-gray-700 rounded-full font-medium">${meta.type}</span>
                ${meta.amount ? `<span class="text-xs px-2.5 py-1 bg-gray-100 text-gray-700 rounded-full font-medium">¥${meta.amount.toLocaleString()}</span>` : ''}
            </div>
        ` : '';

        messageDiv.innerHTML = `
            <div class="flex justify-start items-start gap-3">
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                    <i data-lucide="sparkles" class="w-4 h-4 text-gray-400"></i>
                </div>
                <div class="bg-gray-50 text-gray-900 rounded-xl px-5 py-3.5 max-w-[75%]">
                    <p class="text-base leading-relaxed">${escapeHtml(text)}</p>
                    ${metaInfo}
                </div>
            </div>
        `;
    }

    container.appendChild(messageDiv);

    // Lucideアイコンを初期化
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // スクロール
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * タイピングインジケーター表示
 */
function showTypingIndicator() {
    const container = document.getElementById('chatContainer').querySelector('.max-w-3xl');
    const indicator = document.createElement('div');
    indicator.id = 'typingIndicator';
    indicator.className = 'message-fade-in';
    indicator.innerHTML = `
        <div class="flex justify-start items-start gap-3">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                <i data-lucide="sparkles" class="w-4 h-4 text-gray-400"></i>
            </div>
            <div class="bg-gray-50 text-gray-900 rounded-xl px-5 py-3.5">
                <div class="flex gap-1">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    container.appendChild(indicator);

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * タイピングインジケーター非表示
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// ============================================
// Utility Functions
// ============================================

/**
 * 数値を更新
 */
function updateNumber(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = value;
    }
}

/**
 * HTML エスケープ
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
