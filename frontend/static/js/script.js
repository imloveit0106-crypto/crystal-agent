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
    console.log('Crystal Agent initialized');
    await loadStats();
    await checkConnection();
    setupEventListeners();
});

// ============================================
// Event Listeners
// ============================================

function setupEventListeners() {
    // Enterキーでの送信
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

/**
 * メッセージ送信（グローバル関数）
 */
window.sendMessage = async function() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message) {
        // 空送信時のエラー表示
        input.classList.add('ring-2', 'ring-red-500/50');
        setTimeout(() => {
            input.classList.remove('ring-2', 'ring-red-500/50');
        }, 500);
        return;
    }

    // ユーザーメッセージを表示
    addMessage(message, 'user');

    // 入力欄をクリア
    input.value = '';

    // タイピングインジケーター表示
    showTypingIndicator();

    try {
        const data = await sendChatMessage(message);
        hideTypingIndicator();

        // AIメッセージを表示
        addMessage(data.response, 'assistant');

        // 統計を更新
        await loadStats();

    } catch (error) {
        hideTypingIndicator();
        addMessage('エラーが発生しました。もう一度お試しください。', 'assistant');
        console.error('Send message error:', error);
    }
}

/**
 * クイック入力（グローバル関数）
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

        console.log('Connection check:', data);
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

        // Update total count
        updateNumber('totalCount', stats.total);

        // Update diary count (日記タイプ)
        const diaryCount = stats.types['日記'] || 0;
        updateNumber('diaryCount', diaryCount);

        // Update task count (タスクタイプ)
        const taskCount = stats.types['タスク'] || 0;
        updateNumber('taskCount', taskCount);

        console.log('統計データ取得:', stats);
    } catch (error) {
        console.error('Stats load failed:', error);
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

        console.log('チャット応答:', data);
        console.log('RAG使用:', data.rag_used ? 'はい' : 'いいえ');

        return data;
    } catch (error) {
        console.error('Chat error:', error);
        throw error;
    }
}

// ============================================
// UI Functions
// ============================================

/**
 * フォーム送信ハンドラー - エラーハンドリング強化版
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    // 空送信時のエラーハンドリング - 震えるアニメーション
    if (!message) {
        shakeInput(input);
        return;
    }

    // ユーザーメッセージを表示（強化版アニメーション）
    addMessage(message, 'user');

    // 入力欄をクリア
    input.value = '';

    // 特殊コマンド: 「ステータス」でクリスタルカード表示
    if (message.toLowerCase().includes('ステータス') || message.toLowerCase().includes('status')) {
        showTypingIndicatorEnhanced();

        try {
            // クリスタルカード用API呼び出し
            const statusData = await fetchUserStatus();
            hideTypingIndicator();

            // クリスタルカードを表示（SF映画風）
            renderCrystalCard(statusData);

            return; // 通常のチャット処理をスキップ
        } catch (error) {
            hideTypingIndicator();
            addMessage('ステータス情報の取得に失敗しました。', 'assistant');
            return;
        }
    }

    // タイピングインジケーターを表示（強化版）
    showTypingIndicatorEnhanced();

    try {
        // 通常のAPIリクエスト
        const data = await sendChatMessage(message);

        // タイピングインジケーターを非表示
        hideTypingIndicator();

        // AIメッセージを表示（強化版アニメーション）
        addMessage(data.response, 'assistant', {
            type: data.detected_type,
            amount: data.detected_amount,
            saved: data.saved_to_notion
        });

        // 統計を更新（スムーズアニメーション）
        await loadStats();

    } catch (error) {
        hideTypingIndicator();
        addMessage('申し訳ございません。接続エラーが発生しました。', 'assistant');
    }
}

/**
 * メッセージを追加 - White Minimal Design
 */
function addMessage(text, role, meta = {}) {
    const container = document.getElementById('chatContainer').querySelector('.max-w-3xl');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-fade-in';

    const now = new Date().toLocaleTimeString('ja-JP', {
        hour: '2-digit',
        minute: '2-digit'
    });

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

    // Lucideアイコンを初期化（新しく追加されたメッセージ用）
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
 * 下までスクロール - 基本版
 */
function scrollToBottom() {
    scrollToBottomSmooth();
}

/**
 * 下までスクロール - 洗練されたスムーズスクロール
 */
function scrollToBottomSmooth() {
    const messagesContainer = document.getElementById('chatMessages');

    // より自然なスクロール体験
    requestAnimationFrame(() => {
        messagesContainer.scrollTo({
            top: messagesContainer.scrollHeight,
            behavior: 'smooth'
        });
    });
}

// ============================================
// Animation Functions
// ============================================

/**
 * 数値を更新（シンプル版）
 */
function updateNumber(elementId, value) {
    const element = document.getElementById(elementId);
    if (!element) return;
    element.textContent = value;
}

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
// Error Handling & Special Effects
// ============================================

/**
 * 入力欄を震わせる（空送信時）
 */
function shakeInput(inputElement) {
    // エラー状態を追加
    inputElement.classList.add('shake', 'input-error');

    // プレースホルダーを一時的に変更してフィードバック
    const originalPlaceholder = inputElement.placeholder;
    inputElement.placeholder = 'メッセージを入力してください';

    // アニメーション完了後にクラスを削除
    setTimeout(() => {
        inputElement.classList.remove('shake', 'input-error');
        inputElement.placeholder = originalPlaceholder;
    }, 500);

    // フォーカスを当てて再入力を促す
    inputElement.focus();
}

/**
 * 強化版タイピングインジケーター表示
 */
function showTypingIndicatorEnhanced() {
    const indicator = document.getElementById('typingIndicator');

    // 既存のドットを強化版に置き換え
    const typingContainer = indicator.querySelector('.typing-indicator');
    if (typingContainer) {
        typingContainer.innerHTML = `
            <div class="typing-dot-enhanced"></div>
            <div class="typing-dot-enhanced"></div>
            <div class="typing-dot-enhanced"></div>
        `;
    }

    indicator.classList.remove('hidden');
    scrollToBottomSmooth();
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

    // 微細なフィードバック：入力欄を一瞬ハイライト
    input.classList.add('focus-ring');
    setTimeout(() => {
        input.classList.remove('focus-ring');
    }, 200);
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
// Crystal Status Card - SF Movie Hologram
// ============================================

/**
 * ユーザーステータスを取得
 */
async function fetchUserStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/status`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('ステータスデータ取得:', data);
        return data;
    } catch (error) {
        console.error('Status fetch error:', error);
        throw error;
    }
}

/**
 * クリスタルカードをレンダリング（SF映画風ホログラム）
 */
function renderCrystalCard(statusData) {
    const messagesContainer = document.getElementById('chatMessages');
    const cardContainer = document.createElement('div');
    cardContainer.className = 'crystal-card-container message-enter-advanced';

    // クリスタルカードHTML生成
    cardContainer.innerHTML = `
        <div class="crystal-card crystal-card-reveal" id="crystal-card-${Date.now()}">
            <!-- ヘッダー -->
            <div class="crystal-card-header">
                <div class="crystal-card-name">${escapeHtml(statusData.name)}</div>
            </div>

            <!-- 情報グリッド -->
            <div class="crystal-card-grid">
                <!-- 年齢 -->
                <div class="crystal-card-item">
                    <div class="crystal-card-label">Age</div>
                    <div class="crystal-card-value">${statusData.age}</div>
                </div>

                <!-- MBTI -->
                <div class="crystal-card-item">
                    <div class="crystal-card-label">MBTI</div>
                    <div class="crystal-card-value">${escapeHtml(statusData.mbti)}</div>
                </div>

                <!-- パーソナルカラー -->
                <div class="crystal-card-item">
                    <div class="crystal-card-label">Color Type</div>
                    <div class="crystal-card-value">${escapeHtml(statusData.color)}</div>
                </div>

                <!-- ゴール（全幅） -->
                <div class="crystal-card-goal">
                    <div class="crystal-card-goal-label">Target Goal</div>
                    <div class="crystal-card-goal-value">${escapeHtml(statusData.goal)}</div>
                </div>
            </div>
        </div>
    `;

    messagesContainer.appendChild(cardContainer);

    // Dynamic Lighting効果をセットアップ
    const card = cardContainer.querySelector('.crystal-card');
    setupCardDynamicLighting(card);

    scrollToBottomSmooth();
}

/**
 * Dynamic Lighting - マウス位置に応じた光沢効果
 */
function setupCardDynamicLighting(cardElement) {
    cardElement.addEventListener('mousemove', (e) => {
        const rect = cardElement.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;

        // CSS変数を更新して光沢位置を変更
        cardElement.style.setProperty('--mouse-x', `${x}%`);
        cardElement.style.setProperty('--mouse-y', `${y}%`);
    });

    // カードから離れたら中央にリセット
    cardElement.addEventListener('mouseleave', () => {
        cardElement.style.setProperty('--mouse-x', '50%');
        cardElement.style.setProperty('--mouse-y', '50%');
    });
}

// ============================================
// Export for Global Access
// ============================================

// グローバル関数として公開（HTMLから呼び出せるように）
window.quickInput = quickInput;
window.loadStats = loadStats;
window.checkConnection = checkConnection;
window.fetchUserStatus = fetchUserStatus;
