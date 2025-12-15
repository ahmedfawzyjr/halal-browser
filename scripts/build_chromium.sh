#!/bin/bash

# Halal Browser - Chromium Build Script
# This script clones and builds Chromium

set -e  # Exit on error

echo "=================================================="
echo "🌙 Halal Browser - Chromium Build"
echo "=================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROMIUM_DIR="$PROJECT_ROOT/chromium-core"
BUILD_TYPE="${1:-Default}"  # Default or Release

echo -e "${BLUE}Project root: $PROJECT_ROOT${NC}"
echo -e "${BLUE}Chromium directory: $CHROMIUM_DIR${NC}"
echo -e "${BLUE}Build type: $BUILD_TYPE${NC}"

# Check depot_tools
if ! command -v gclient &> /dev/null; then
    echo -e "${RED}❌ depot_tools not found in PATH${NC}"
    echo "   Please run setup_env.sh first"
    exit 1
fi

echo ""
echo "⚠️  WARNING: Chromium build requires:"
echo "   - 100GB+ free disk space"
echo "   - 16GB+ RAM (32GB recommended)"
echo "   - 2-4 hours for first build"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Create chromium directory
mkdir -p "$CHROMIUM_DIR"
cd "$CHROMIUM_DIR"

echo ""
echo "📥 Step 1: Cloning Chromium source..."
if [ ! -d "src" ]; then
    echo "   This will download ~20GB of data..."
    git clone https://chromium.googlesource.com/chromium/src.git
    echo -e "${GREEN}✅ Chromium source cloned${NC}"
else
    echo -e "${YELLOW}⚠️  Chromium source already exists${NC}"
    cd src
    git pull origin main
    cd ..
fi

cd src

echo ""
echo "📥 Step 2: Syncing dependencies..."
echo "   This will download ~40GB total..."
gclient sync

echo ""
echo "⚙️  Step 3: Configuring build..."

# Create build configuration
mkdir -p "out/$BUILD_TYPE"

cat > "out/$BUILD_TYPE/args.gn" << EOF
# Halal Browser Build Configuration

# Build type
is_debug = false
is_component_build = true

# Optimization
symbol_level = 1
blink_symbol_level = 0
remove_webcore_debug_symbols = true

# Features to disable (reduce build time)
enable_nacl = false
enable_remoting = false
enable_reporting = false
enable_service_discovery = false

# Branding
chrome_pgo_phase = 0

# Performance
use_jumbo_build = true
EOF

echo -e "${GREEN}✅ Build configuration created${NC}"
cat "out/$BUILD_TYPE/args.gn"

echo ""
echo "🔧 Step 4: Generating build files..."
gn gen "out/$BUILD_TYPE"

echo ""
echo "🏗️  Step 5: Building Chromium..."
echo "   This will take 2-4 hours on first build..."
echo "   Subsequent builds will be much faster (incremental)"
echo ""

# Get number of CPU cores
CORES=$(nproc)
echo "   Using $CORES CPU cores"

# Build Chrome
ninja -C "out/$BUILD_TYPE" chrome -j$CORES

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Chromium build completed!${NC}"
echo "=================================================="
echo ""
echo "🚀 To run Chromium:"
echo "   cd $CHROMIUM_DIR/src"
echo "   ./out/$BUILD_TYPE/chrome"
echo ""
echo "📝 Next steps:"
echo "   1. Test the browser"
echo "   2. Customize branding (name, icon)"
echo "   3. Integrate Halal filtering extension"
echo ""
