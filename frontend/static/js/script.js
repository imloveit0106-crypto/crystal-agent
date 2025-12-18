/**
 * Crystal Agent - Frontend JavaScript
 * Apple Quality Chat Interface
 */

// ============================================
// Configuration
// ============================================

const API_BASE_URL = 'http://localhost:8000';

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🔮 Crystal Agent initialized');
    await loadStats();
    await checkConnection();
    setupEventListeners();
});

// ============================================
// Event Listeners
// ============================================

function setupEventListeners() {
    // フォーム送信
    document.getElementById('chatForm').addEventListener('submit', handleFormSubmit);

    // Enterキーでの送信（Shift+Enterは改行）
    document.getElementById('messageInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleFormSubmit(e);
        }
    });
}

// ============================================
// API Functions
// ============================================

/**
 * 接続チェック
 */
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();

        const statusIndicator = document.getElementById('statusIndicator');

        if (data.notion === 'connected' && data.gemini === 'connected') {
            statusIndicator.innerHTML = `
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-xs font-semibold text-green-700">Online</span>
            `;
            statusIndicator.className = 'flex items-center gap-2 px-4 py-2 bg-green-50 rounded-full';
        } else {
            statusIndicator.innerHTML = `
                <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span class="text-xs font-semibold text-yellow-700">Limited</span>
            `;
            statusIndicator.className = 'flex items-center gap-2 px-4 py-2 bg-yellow-50 rounded-full';
        }

        console.log('✅ Connection check:', data);
    } catch (error) {
        console.error('❌ Connection check failed:', error);
        const statusIndicator = document.getElementById('statusIndicator');
        statusIndicator.innerHTML = `
            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
            <span class="text-xs font-semibold text-red-700">Offline</span>
        `;
        statusIndicator.className = 'flex items-center gap-2 px-4 py-2 bg-red-50 rounded-full';
    }
}

/**
 * 統計データ読み込み
 */
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const stats = await response.json();

        // アニメーション付きで数値を更新
        animateNumber('statTotal', stats.total);

        const totalAmount = stats.amounts.reduce((sum, amt) => sum + amt, 0);
        animateNumber('statAmount', totalAmount, '¥');

        animateNumber('statTypes', Object.keys(stats.types).length);

        console.log('📊 統計データ取得:', stats);
    } catch (error) {
        console.error('❌ Stats load failed:', error);
    }
}

/**
 * チャットメッセージ送信
 */
async function sendChatMessage(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                use_rag: true
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        console.log('💬 チャット応答:', data);
        console.log('🔍 RAG使用:', data.rag_used ? 'はい' : 'いいえ');

        return data;
    } catch (error) {
        console.error('❌ Chat error:', error);
        throw error;
    }
}

// ============================================
// UI Functions
// ============================================

/**
 * フォーム送信ハンドラー
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message) return;

    // ユーザーメッセージを表示
    addMessage(message, 'user');

    // 入力欄をクリア
    input.value = '';

    // タイピングインジケーターを表示
    showTypingIndicator();

    try {
        // APIリクエスト
        const data = await sendChatMessage(message);

        // タイピングインジケーターを非表示
        hideTypingIndicator();

        // AIメッセージを表示
        addMessage(data.response, 'assistant', {
            type: data.detected_type,
            amount: data.detected_amount,
            saved: data.saved_to_notion
        });

        // 統計を更新
        await loadStats();

    } catch (error) {
        hideTypingIndicator();
        addMessage('申し訳ございません。接続エラーが発生しました。', 'assistant');
    }
}

/**
 * メッセージを追加
 */
function addMessage(text, role, meta = {}) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-enter';

    const now = new Date().toLocaleTimeString('ja-JP', {
        hour: '2-digit',
        minute: '2-digit'
    });

    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="flex gap-3 items-end justify-end">
                <div class="flex flex-col items-end max-w-md">
                    <div class="relative bg-gradient-to-r from-blue-500 to-blue-600 message-tail-user rounded-3xl rounded-br-md px-6 py-4 shadow-lg" style="border-left-color: #3b82f6;">
                        <p class="text-white leading-relaxed">${escapeHtml(text)}</p>
                    </div>
                    <span class="text-xs text-gray-400 mt-2 mr-2">あなた • ${now}</span>
                </div>
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center shadow-lg flex-shrink-0">
                    <span class="text-xl">👤</span>
                </div>
            </div>
        `;
    } else {
        const metaInfo = meta.saved ? `
            <div class="flex gap-2 mt-3">
                <span class="px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full font-semibold">✓ ${meta.type}</span>
                ${meta.amount ? `<span class="px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-semibold">¥${meta.amount.toLocaleString()}</span>` : ''}
            </div>
        ` : '';

        messageDiv.innerHTML = `
            <div class="flex gap-3 items-end">
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white shadow-lg flex-shrink-0">
                    <span class="text-xl">🤖</span>
                </div>
                <div class="flex flex-col max-w-md">
                    <div class="relative bg-white message-tail-ai rounded-3xl rounded-bl-md px-6 py-4 shadow-apple">
                        <p class="text-gray-800 leading-relaxed">${escapeHtml(text)}</p>
                        ${metaInfo}
                    </div>
                    <span class="text-xs text-gray-400 mt-2 ml-2">Crystal Agent • ${now}</span>
                </div>
            </div>
        `;
    }

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * タイピングインジケーター表示
 */
function showTypingIndicator() {
    document.getElementById('typingIndicator').classList.remove('hidden');
    scrollToBottom();
}

/**
 * タイピングインジケーター非表示
 */
function hideTypingIndicator() {
    document.getElementById('typingIndicator').classList.add('hidden');
}

/**
 * 下までスクロール
 */
function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
    });
}

// ============================================
// Animation Functions
// ============================================

/**
 * 数値アニメーション（カウントアップ）
 */
function animateNumber(elementId, targetValue, prefix = '') {
    const element = document.getElementById(elementId);
    if (!element) return;

    const duration = 1000;
    const steps = 30;
    const stepValue = targetValue / steps;
    let currentValue = 0;

    const timer = setInterval(() => {
        currentValue += stepValue;
        if (currentValue >= targetValue) {
            currentValue = targetValue;
            clearInterval(timer);
        }
        element.textContent = prefix + Math.floor(currentValue).toLocaleString();
    }, duration / steps);
}

// ============================================
// Utility Functions
// ============================================

/**
 * クイック入力
 */
function quickInput(text) {
    const input = document.getElementById('messageInput');
    input.value = text;
    input.focus();
}

/**
 * HTML エスケープ
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * フォーマット日時
 */
function formatDateTime(date) {
    return new Intl.DateTimeFormat('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// ============================================
// Export for Global Access
// ============================================

// グローバル関数として公開（HTMLから呼び出せるように）
window.quickInput = quickInput;
window.loadStats = loadStats;
window.checkConnection = checkConnection;
