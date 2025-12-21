#!/bin/bash
# Crystal Agent - Simple Startup Script

echo "============================================================"
echo "🔮 Crystal Agent - Starting Server..."
echo "============================================================"

# Navigate to project directory
cd "$(dirname "$0")/crystal-agent-main"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv .venv
fi

# Activate virtual environment (optional)
# source .venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt --quiet
fi

# Start the server
echo ""
echo "✨ Starting FastAPI server..."
echo "🌐 Open http://localhost:8000 in your browser"
echo ""

python backend/main.py
