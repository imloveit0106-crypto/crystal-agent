# 🚀 Crystal Agent - Streaming Chat

## Commercial-Grade Real-Time Chat Experience

Crystal Agent now features a **commercial-grade streaming chat interface** with ChatGPT-like real-time responses.

---

## ✨ Features

### 🎯 Real-Time Streaming
- **Server-Sent Events (SSE)** for instant message delivery
- **Typewriter effect** - AI "types" responses character by character
- **60fps smooth performance** - Optimized animations and rendering

### 📝 Rich Text Support
- **Markdown rendering** with Marked.js
- **Syntax highlighting** with Highlight.js
- Support for:
  - Headers, lists, blockquotes
  - Code blocks with syntax highlighting
  - Links, bold, italic
  - Tables and more

### 🎨 Premium UI/UX
- **Glassmorphism 2.0** - Frosted glass effects with backdrop filters
- **Physics-based micro-interactions** - Spring animations on hover/click
- **Responsive design** - Works on desktop, tablet, and mobile
- **Auto-scroll** - Smoothly follows conversation

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python manage.py --install
```

### 2. Launch Streaming Chat

```bash
python manage.py --streaming
```

The streaming chat server will start at **http://localhost:8000**

### 3. Launch Traditional Streamlit App (optional)

```bash
python manage.py
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│   Frontend (HTML/CSS/JS)                │
│   - Vanilla JavaScript                  │
│   - Marked.js (Markdown)                │
│   - Highlight.js (Syntax highlighting) │
│   - Fetch API + SSE                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   FastAPI Backend (Python)              │
│   - Streaming endpoints                 │
│   - Server-Sent Events (SSE)            │
│   - Gemini AI integration               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Google Gemini 1.5 Flash               │
│   - Streaming responses                 │
│   - Context-aware AI                    │
└─────────────────────────────────────────┘
```

---

## 📚 API Endpoints

### `GET /`
Main chat interface (HTML page)

### `POST /api/chat`
Standard non-streaming chat endpoint

**Request:**
```json
{
  "message": "Hello, how are you?",
  "user_id": "default_user"
}
```

**Response:**
```json
{
  "response": "I'm doing great! How can I help you today?",
  "type": "日記",
  "emotion": "良好",
  "amount": null
}
```

### `POST /api/chat/stream`
**Streaming chat endpoint** using Server-Sent Events

**Request:**
```json
{
  "message": "Explain quantum computing",
  "user_id": "default_user"
}
```

**SSE Response Stream:**
```
data: {"type": "metadata", "detected_type": "日記", "detected_emotion": "普通"}

data: {"chunk": "Quantum", "done": false}

data: {"chunk": " computing", "done": false}

data: {"chunk": " is...", "done": false}

data: {"chunk": "", "done": true}
```

### `GET /api/stats`
Get user statistics

**Response:**
```json
{
  "total_logs": 42,
  "by_type": {
    "タスク": 10,
    "支出": 8,
    "日記": 20,
    "悩み": 4
  },
  "total_amount": 15000
}
```

### `GET /api/logs?limit=10`
Get recent logs

### `GET /health`
Health check endpoint

---

## 🎨 UI Components

### Chat Messages
- **User messages** - Right-aligned with user avatar
- **AI messages** - Left-aligned with Crystal Agent avatar
- **Type badges** - Auto-detected message type (日記, 支出, タスク, 悩み)
- **Markdown rendering** - Rich text formatting
- **Code highlighting** - Beautiful syntax-highlighted code blocks

### Sidebar
- **Real-time statistics** - Total logs, tasks, spending
- **Quick actions** - One-click templates for common actions
- **Connection status** - Live server connection indicator

### Input Area
- **Modern text input** - Glassmorphism design
- **Send button** - Gradient button with hover effects
- **Typing indicator** - Shows when AI is responding

---

## 🎯 Performance Optimizations

### 60fps Rendering
- `requestAnimationFrame` for smooth animations
- Debounced scroll events
- GPU-accelerated CSS transforms
- Efficient DOM updates

### Streaming Optimizations
- Chunk-based rendering (no full reflow)
- Incremental markdown parsing
- Lazy syntax highlighting
- Connection keep-alive

### Network Optimizations
- SSE with automatic reconnection
- Compression headers
- CDN for libraries (Marked.js, Highlight.js)

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Gemini API Key (required for AI features)
GEMINI_API_KEY=your_gemini_api_key_here

# Notion API (optional)
NOTION_API_KEY=your_notion_api_key
NOTION_USER_PROFILE_DB_ID=your_database_id
NOTION_LIFE_LOG_DB_ID=your_database_id
```

### Server Configuration

Edit `backend/main.py`:

```python
# Change port
uvicorn.run("main:app", host="0.0.0.0", port=8000)

# Enable auto-reload (development)
uvicorn.run("main:app", reload=True)

# Production settings
uvicorn.run("main:app", workers=4, log_level="info")
```

---

## 📦 Deployment

### Local Development
```bash
python manage.py --streaming
```

### Production (Docker)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "backend/main.py"]
```

Build and run:
```bash
docker build -t crystal-agent .
docker run -p 8000:8000 --env-file .env crystal-agent
```

### Cloud Deployment

**Recommended platforms:**
- **Render** - Easy deployment, free tier available
- **Railway** - Auto-scaling, great for FastAPI
- **Heroku** - Simple deployment process
- **Google Cloud Run** - Serverless, pay-per-use

---

## 🎓 Technical Details

### Streaming Implementation

The streaming chat uses **Server-Sent Events (SSE)**, which is simpler than WebSockets for one-way server-to-client communication.

**Backend (Python/FastAPI):**
```python
async def stream_response():
    for chunk in gemini_response:
        yield f"data: {json.dumps({'chunk': chunk})}\n\n"

return StreamingResponse(stream_response(), media_type="text/event-stream")
```

**Frontend (JavaScript):**
```javascript
const response = await fetch('/api/chat/stream', {
    method: 'POST',
    body: JSON.stringify({ message })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    // Process and render chunk
}
```

### Markdown Rendering

Uses **Marked.js** with custom configuration:

```javascript
marked.setOptions({
    breaks: true,  // Support line breaks
    gfm: true,     // GitHub Flavored Markdown
    highlight: (code, lang) => {
        return hljs.highlight(code, { language: lang }).value;
    }
});
```

### Syntax Highlighting

Uses **Highlight.js** with Atom One Dark theme:

```javascript
// Auto-detect language
hljs.highlightAuto(code)

// Specific language
hljs.highlight(code, { language: 'python' })
```

---

## 🐛 Troubleshooting

### "Repository not found" during git push
The `origin` remote is pointing to a local proxy that may not be available. Use the `personal` remote instead:
```bash
git push personal <branch-name>
```

### Port 8000 already in use
Change the port in `backend/main.py`:
```python
uvicorn.run("main:app", port=8080)  # Use different port
```

### AI not responding
1. Check `.env` file has valid `GEMINI_API_KEY`
2. Check API quota at https://makersuite.google.com/app/apikey
3. Check server logs for errors

### Streaming not working
1. Check browser console for errors
2. Verify CORS settings in `backend/main.py`
3. Test with `/health` endpoint first
4. Check network tab in browser DevTools

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Streamlit** - Original UI framework
- **FastAPI** - High-performance web framework
- **Google Gemini** - AI language model
- **Marked.js** - Markdown parser
- **Highlight.js** - Syntax highlighting
- **Inter Font** - Beautiful typography

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review `docs/SYSTEM_ARCHITECTURE.md`
3. Check `docs/DEMO_PRESENTATION.md`
4. Open an issue on GitHub

---

**Built with ❤️ for a commercial-grade AI chat experience**
