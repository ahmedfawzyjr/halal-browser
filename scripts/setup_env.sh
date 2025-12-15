#!/bin/bash

# Halal Browser - Environment Setup Script
# This script sets up the development environment for building Halal Browser

set -e  # Exit on error

echo "=================================================="
echo "🌙 Halal Browser - Environment Setup"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ This script is designed for Linux (Ubuntu/Debian)${NC}"
    echo "   For other systems, please install dependencies manually"
    exit 1
fi

echo -e "${GREEN}✅ Running on Linux${NC}"

# Check for sudo privileges
if ! sudo -v; then
    echo -e "${RED}❌ This script requires sudo privileges${NC}"
    exit 1
fi

echo ""
echo "📦 Step 1: Updating system packages..."
sudo apt update

echo ""
echo "📦 Step 2: Installing build essentials..."
sudo apt install -y \
    build-essential \
    clang \
    cmake \
    ninja-build \
    pkg-config \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    wget

echo ""
echo "📦 Step 3: Installing Chromium dependencies..."
sudo apt install -y \
    libgtk-3-dev \
    libnss3-dev \
    libasound2-dev \
    libxss-dev \
    libxtst-dev \
    libpci-dev \
    libglib2.0-dev \
    libdbus-1-dev \
    libatk1.0-dev \
    libatk-bridge2.0-dev \
    libcups2-dev \
    libdrm-dev \
    libxkbcommon-dev \
    libxcomposite-dev \
    libxdamage-dev \
    libxrandr-dev \
    libgbm-dev \
    libpango1.0-dev \
    libcairo2-dev

echo ""
echo "📦 Step 4: Installing depot_tools..."
if [ ! -d "$HOME/depot_tools" ]; then
    cd "$HOME"
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    echo -e "${GREEN}✅ depot_tools installed${NC}"
else
    echo -e "${YELLOW}⚠️  depot_tools already exists, skipping...${NC}"
fi

# Add depot_tools to PATH
if ! grep -q "depot_tools" "$HOME/.bashrc"; then
    echo 'export PATH="$HOME/depot_tools:$PATH"' >> "$HOME/.bashrc"
    echo -e "${GREEN}✅ Added depot_tools to PATH${NC}"
fi

export PATH="$HOME/depot_tools:$PATH"

echo ""
echo "📦 Step 5: Setting up Python virtual environment..."
cd "$(dirname "$0")/.."  # Go to project root

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

source venv/bin/activate

echo ""
echo "📦 Step 6: Installing Python dependencies..."
pip install --upgrade pip
pip install -r ai-service/requirements.txt

echo ""
echo "📦 Step 7: Creating necessary directories..."
mkdir -p chromium-core
mkdir -p ai-service/models
mkdir -p ai-service/cache
mkdir -p tests/data
mkdir -p logs

echo ""
echo "📥 Step 8: Downloading AI models..."
if [ ! -f "ai-service/models/nsfw_model.onnx" ]; then
    echo "   Downloading OpenNSFW2 model..."
    wget -q --show-progress \
        https://github.com/bhky/opennsfw2/releases/download/v0.10.0/nsfw_model.onnx \
        -O ai-service/models/nsfw_model.onnx
    echo -e "${GREEN}✅ Model downloaded${NC}"
else
    echo -e "${YELLOW}⚠️  Model already exists${NC}"
fi

echo ""
echo "🧪 Step 9: Testing installations..."

# Test depot_tools
if command -v gclient &> /dev/null; then
    echo -e "${GREEN}✅ gclient: $(gclient --version)${NC}"
else
    echo -e "${RED}❌ gclient not found${NC}"
fi

if command -v gn &> /dev/null; then
    echo -e "${GREEN}✅ gn: $(gn --version)${NC}"
else
    echo -e "${RED}❌ gn not found${NC}"
fi

if command -v ninja &> /dev/null; then
    echo -e "${GREEN}✅ ninja: $(ninja --version)${NC}"
else
    echo -e "${RED}❌ ninja not found${NC}"
fi

# Test Python packages
python3 -c "import onnxruntime; print('✅ onnxruntime:', onnxruntime.__version__)"
python3 -c "import cv2; print('✅ opencv:', cv2.__version__)"
python3 -c "import flask; print('✅ flask:', flask.__version__)"

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Environment setup completed!${NC}"
echo "=================================================="
echo ""
echo "📝 Next steps:"
echo "   1. Run: source venv/bin/activate"
echo "   2. Run: ./scripts/build_chromium.sh"
echo "   3. Run: python3 ai-service/api_server.py"
echo ""
echo "📖 See docs/ROADMAP.md for detailed instructions"
echo ""
