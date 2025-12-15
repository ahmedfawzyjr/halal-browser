#!/bin/bash

# Halal Browser - Start AI Service
# Starts the local AI filtering service

set -e

echo "=================================================="
echo "🤖 Starting Halal Browser AI Service"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Get project root
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo "   Please run: ./scripts/setup_env.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if model exists
if [ ! -f "ai-service/models/nsfw_model.onnx" ]; then
    echo -e "${RED}❌ AI model not found${NC}"
    echo "   Please run: ./scripts/setup_env.sh"
    exit 1
fi

# Start AI service
echo -e "${GREEN}✅ Starting AI Service on http://127.0.0.1:5000${NC}"
echo ""
cd ai-service
python3 api_server.py
