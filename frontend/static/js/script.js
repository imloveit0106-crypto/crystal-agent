/**
 * Crystal Agent - Frontend JavaScript
 * Minimal & Clean Implementation
 */

// ============================================
// Configuration
// ============================================

const API_BASE_URL = 'http://localhost:8000';

// Scenario D: 連打防止フラグ（Debouncing）
let isSendingMessage = false;

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Crystal Agent initialized');
    await loadStats();
    await checkConnection();
    setupEventListeners();

    // 初回訪問時のヘルプモーダル自動表示
    checkFirstVisit();
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
 * メッセージ送信 (Expense Detection & API Integration)
 */
window.sendMessage = async function() {
    // Scenario D: 連打防止（Debouncing）
    if (isSendingMessage) {
        console.log('⚠️ 送信処理中です。しばらくお待ちください。');
        return;
    }

    const input = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const message = input.value.trim();

    if (!message) {
        input.classList.add('ring-2', 'ring-red-500');
        setTimeout(() => input.classList.remove('ring-2', 'ring-red-500'), 500);
        return;
    }

    // 送信フラグをセット（連打防止）
    isSendingMessage = true;

    // ウェルカムスクリーンを非表示（初回のみ）
    const welcomeScreen = document.getElementById('welcomeScreen');
    if (welcomeScreen && welcomeScreen.style.display !== 'none') {
        // サジェストと同じオーケストレーション実行
        await hideWelcomeScreenWithAnimation();
    }

    // Loading State: 送信ボタンを無効化
    if (sendButton) {
        sendButton.disabled = true;
        sendButton.style.opacity = '0.7';
    }

    addMessage(message, 'user');
    input.value = '';
    showTypingIndicator();

    try {
        // 支出情報を検出
        const expenseData = parseExpenseFromMessage(message);

        // 支出データがあればNotionに送信
        if (expenseData) {
            try {
                const expenseResult = await sendExpenseToBackend(
                    expenseData.item,
                    expenseData.amount,
                    expenseData.category
                );
                console.log('Expense saved to Notion:', expenseResult);
                showToast('Saved to Notion', 'success');
            } catch (expenseError) {
                console.error('Expense save error:', expenseError);
                showToast('Failed to save expense', 'error');
            }
        }

        // AIチャット応答を取得（既存フロー）
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
        showToast('Error occurred', 'error');
    } finally {
        // Loading State: 送信ボタンを再有効化
        if (sendButton) {
            sendButton.disabled = false;
            sendButton.style.opacity = '1';
        }
        // Scenario D: 送信フラグをリセット（次のメッセージを許可）
        isSendingMessage = false;
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

/**
 * サジェストチップから送信
 * 画面遷移とAPI通信を並行処理するオーケストレーター
 */
window.sendSuggest = async function(prompt) {
    // Step 1-4: Welcome Screen Exit & Chat Area Enter
    // 高精細アニメーションでウェルカムスクリーンを非表示
    await hideWelcomeScreenWithAnimation();

    // Step 5: Interaction Feedback (Optimistic UI)
    // ユーザー入力を即時反映し、ローディングを開始
    addMessage(prompt, 'user');
    showTypingIndicator();

    // Step 6: API Request
    try {
        const data = await sendChatMessage(prompt);
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

// ============================================
// API Functions
// ============================================

/**
 * 接続チェック (Updated for new API structure)
 */
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        const statusIndicator = document.getElementById('statusIndicator');

        // New API structure: data.services.notion, data.services.gemini
        const services = data.services || data;
        const notionStatus = services.notion || data.notion;
        const geminiStatus = services.gemini || data.gemini;

        if (notionStatus === 'connected' && geminiStatus === 'connected') {
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

/**
 * 支出データをNotionバックエンドに送信 (Fetch API)
 * @param {string} item - 支出項目の説明
 * @param {number} amount - 金額（正の整数）
 * @param {string} category - カテゴリー（デフォルト: "支出"）
 * @returns {Promise<Object>} APIレスポンス
 */
async function sendExpenseToBackend(item, amount, category = "支出") {
    const response = await fetch(`${API_BASE_URL}/api/notion/expense`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            item: String(item),
            amount: parseInt(amount, 10),
            category: String(category)
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`);
    }

    return data;
}

/**
 * メッセージから支出情報を抽出
 * @param {string} text - ユーザーメッセージ
 * @returns {Object|null} {item, amount, category} または null
 */
function parseExpenseFromMessage(text) {
    // 金額パターン: "800円", "¥800", "800yen"
    const amountPattern = /(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:円|¥|yen)/i;
    const amountMatch = text.match(amountPattern);

    if (!amountMatch) {
        return null; // 金額が見つからない
    }

    const amount = parseInt(amountMatch[1].replace(/,/g, ''), 10);

    // カテゴリー推測
    let category = "支出";
    if (text.includes('ランチ') || text.includes('食事') || text.includes('飲み会') || text.includes('食費')) {
        category = "食費";
    } else if (text.includes('電車') || text.includes('バス') || text.includes('交通')) {
        category = "交通費";
    } else if (text.includes('買い物') || text.includes('購入')) {
        category = "買い物";
    }

    // 項目説明を抽出（金額部分を除く）
    const item = text.replace(amountPattern, '').trim() || `${category} (詳細なし)`;

    return { item, amount, category };
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
                <div class="bg-gray-800 text-white rounded-xl px-5 py-3.5 max-w-[75%]">
                    <p class="text-base leading-relaxed">${escapeHtml(text)}</p>
                </div>
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                    <i data-lucide="user" class="w-4.5 h-4.5 text-gray-400"></i>
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
                    <i data-lucide="sparkles" class="w-4.5 h-4.5 text-gray-400"></i>
                </div>
                <div class="bg-gray-50 text-gray-800 rounded-xl px-5 py-3.5 max-w-[75%]">
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
            <div class="bg-gray-50 text-gray-800 rounded-xl px-5 py-3.5">
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

/**
 * Toast通知を表示 (Success/Error Feedback)
 * @param {string} message - 表示メッセージ
 * @param {string} type - 'success' または 'error'
 */
function showToast(message, type = 'success') {
    // 既存のtoastがあれば削除
    const existingToast = document.getElementById('toast');
    if (existingToast) {
        existingToast.remove();
    }

    // Toast要素を作成
    const toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = `fixed bottom-6 right-6 px-5 py-3.5 rounded-xl shadow-lg flex items-center gap-3 motion-base motion-enter-down z-50 ${
        type === 'success' ? 'bg-gray-800 text-white' : 'bg-red-600 text-white'
    }`;

    // アイコンとメッセージ
    const icon = type === 'success' ? 'check' : 'alert-circle';
    toast.innerHTML = `
        <i data-lucide="${icon}" class="w-4.5 h-4.5"></i>
        <span class="text-sm font-medium">${message}</span>
    `;

    document.body.appendChild(toast);

    // Lucideアイコンを初期化
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // アニメーション: Enter
    requestAnimationFrame(() => {
        toast.classList.remove('motion-enter-down');
        toast.classList.add('motion-active');
    });

    // 3秒後に自動削除
    setTimeout(() => {
        toast.classList.remove('motion-active');
        toast.classList.add('motion-exit-up');
        setTimeout(() => toast.remove(), 600);
    }, 3000);
}

// ============================================
// Utility Functions
// ============================================

/**
 * ウェルカムスクリーンを非表示（旧バージョン・互換性用）
 */
function hideWelcomeScreen() {
    const welcomeScreen = document.getElementById('welcomeScreen');
    if (welcomeScreen && !welcomeScreen.classList.contains('hidden')) {
        welcomeScreen.classList.add('hidden');
        // アニメーション完了後に完全に削除
        setTimeout(() => {
            welcomeScreen.classList.add('gone');
        }, 500);
    }
}

/**
 * ウェルカムスクリーンを高精細アニメーションで非表示
 * 商用プロダクトレベルのオーケストレーション
 */
async function hideWelcomeScreenWithAnimation() {
    const welcomeScreen = document.getElementById('welcomeScreen');
    const chatContainer = document.getElementById('chatContainer');

    if (!welcomeScreen || welcomeScreen.style.display === 'none') {
        return; // 既に非表示なら何もしない
    }

    // UI Lock
    document.body.style.pointerEvents = 'none';

    // Exit Animation
    welcomeScreen.classList.add('motion-base');
    welcomeScreen.classList.remove('motion-active');
    welcomeScreen.classList.add('motion-exit-up');

    // 600msのアニメーション完了を待機
    await new Promise(resolve => setTimeout(resolve, 600));

    // DOM Swapping
    welcomeScreen.style.display = 'none';

    // Enter Animation for Chat Area
    const messageContainer = chatContainer.querySelector('.max-w-3xl');
    if (messageContainer) {
        messageContainer.classList.add('motion-base', 'motion-enter-down');

        // 強制リフロー
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));

        // Active State
        messageContainer.classList.remove('motion-enter-down');
        messageContainer.classList.add('motion-active');
    }

    // UIロック解除
    document.body.style.pointerEvents = 'auto';
}

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

// ============================================
// Help Modal Functions
// ============================================

/**
 * ヘルプモーダルの表示/非表示を切り替え
 */
window.toggleHelpModal = function() {
    const modal = document.getElementById('helpModal');
    if (!modal) return;

    const isHidden = modal.classList.contains('hidden');

    if (isHidden) {
        // 表示
        modal.classList.remove('hidden');
        // Lucide Icons を再初期化（モーダル内のアイコン用）
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    } else {
        // 非表示
        modal.classList.add('hidden');
    }
}

/**
 * 初回訪問チェック & ヘルプモーダル自動表示
 */
function checkFirstVisit() {
    const hasVisited = localStorage.getItem('crystal_agent_visited');

    if (!hasVisited) {
        // 初回訪問
        console.log('初回訪問を検出 - ヘルプモーダルを自動表示');

        // 1秒後にヘルプモーダルを表示（ページ読み込み後の自然なタイミング）
        setTimeout(() => {
            toggleHelpModal();
        }, 1000);

        // 訪問済みフラグをセット
        localStorage.setItem('crystal_agent_visited', 'true');
    }
}
