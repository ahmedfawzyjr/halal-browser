#!/bin/bash

# Halal Browser - Test AI Service
# Tests the AI filtering service

echo "=================================================="
echo "🧪 Testing Halal Browser AI Service"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

API_URL="http://127.0.0.1:5000"

echo ""
echo "1️⃣ Testing health endpoint..."
response=$(curl -s "$API_URL/api/health")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    echo "   Response: $response"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "   Is the AI service running?"
    echo "   Run: ./scripts/start_ai_service.sh"
    exit 1
fi

echo ""
echo "2️⃣ Testing text analyzer..."
response=$(curl -s -X POST "$API_URL/api/scan/text" \
    -H "Content-Type: application/json" \
    -d '{"text": "This is a safe educational text"}')
echo "   Response: $response"

echo ""
echo "3️⃣ Testing text analyzer with Haram keywords..."
response=$(curl -s -X POST "$API_URL/api/scan/text" \
    -H "Content-Type: application/json" \
    -d '{"text": "Visit our casino for gambling"}')
echo "   Response: $response"

echo ""
echo "4️⃣ Testing URL scanner..."
response=$(curl -s -X POST "$API_URL/api/scan/url" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://quran.com"}')
echo "   Response: $response"

echo ""
echo "=================================================="
echo -e "${GREEN}✅ AI Service tests completed${NC}"
echo "=================================================="
echo ""
echo "📝 To test image/video scanning:"
echo "   1. Place test images in tests/data/"
echo "   2. Use curl or Postman to test /api/scan/image"
echo ""
