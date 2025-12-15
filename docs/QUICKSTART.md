# 🚀 Halal Browser - Quick Start Guide

## For Developers

### Prerequisites
- **OS**: Ubuntu 22.04/24.04 (recommended)
- **RAM**: 16GB minimum, 32GB recommended
- **Disk**: 100GB+ free space
- **Time**: 4-6 hours for initial setup

---

## 🏃 Quick Setup (30 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/halal-browser.git
cd halal-browser
```

### 2. Run Setup Script
```bash
chmod +x scripts/*.sh
./scripts/setup_env.sh
```

This will:
- ✅ Install all system dependencies
- ✅ Install depot_tools for Chromium
- ✅ Create Python virtual environment
- ✅ Download AI models
- ✅ Set up project structure

### 3. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 4. Start AI Service
```bash
./scripts/start_ai_service.sh
```

In another terminal:
```bash
./scripts/test_ai_service.sh
```

You should see:
```
✅ Health check passed
✅ AI Service tests completed
```

---

## 🌐 Testing Without Chromium (Quick Test)

You can test the AI filtering service without building Chromium:

### 1. Test Image Scanning
```bash
# Download a test image
wget https://picsum.photos/400/300 -O tests/data/test_image.jpg

# Test with Python
python3 ai-service/image_scanner.py
```

### 2. Test Text Filtering
```bash
python3 ai-service/text_analyzer.py
```

### 3. Test API Service
```bash
# Start service
python3 ai-service/api_server.py

# In another terminal, test with curl
curl http://127.0.0.1:5000/api/health
curl -X POST http://127.0.0.1:5000/api/scan/text \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test"}'
```

---

## 🏗️ Building Chromium (4-6 hours)

### 1. Clone Chromium Source
```bash
./scripts/build_chromium.sh
```

**Warning**: This downloads ~60GB and takes 2-4 hours to build!

### 2. Test Chromium
```bash
cd chromium-core/src
./out/Default/chrome
```

### 3. Install Halal Filter Extension

1. Open Chromium
2. Go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select `halal-browser/ui/extensions/halal-filter/`

### 4. Test Filtering

Visit test sites:
- ✅ Safe: https://wikipedia.org
- ✅ Safe: https://quran.com
- 🛑 Blocked: Sites in blocklist

---

## 📁 Project Structure Overview

```
halal-browser/
├── ai-service/              # AI content filtering
│   ├── image_scanner.py     # Image NSFW detection
│   ├── video_scanner.py     # Video frame analysis
│   ├── text_analyzer.py     # Text keyword filtering
│   └── api_server.py        # REST API service
│
├── filters/                 # Filtering rules
│   ├── keywords.json        # Haram keywords
│   ├── url_blocklist.json   # Blocked domains
│   ├── url_whitelist.json   # Safe domains
│   └── rules_engine.py      # Policy decisions
│
├── profiles/                # User profiles
│   ├── kids_mode.json       # Kids profile
│   ├── family_mode.json     # Family profile
│   ├── adult_mode.json      # Adult profile
│   └── school_mode.json     # School profile
│
├── ui/extensions/           # Browser extension
│   └── halal-filter/        # Content filter extension
│
├── scripts/                 # Build scripts
│   ├── setup_env.sh         # Environment setup
│   ├── build_chromium.sh    # Build Chromium
│   ├── start_ai_service.sh  # Start AI service
│   └── test_ai_service.sh   # Test AI service
│
└── docs/                    # Documentation
    ├── ARCHITECTURE.md      # System architecture
    ├── ROADMAP.md           # Development roadmap
    └── QUICKSTART.md        # This file
```

---

## 🧪 Testing Checklist

### AI Service Tests
- [ ] Health check passes
- [ ] Text filtering works
- [ ] Image scanning works (if model downloaded)
- [ ] URL filtering works

### Browser Tests
- [ ] Chromium builds successfully
- [ ] Browser launches
- [ ] Extension loads
- [ ] Blocked sites redirect to blocked page
- [ ] Safe sites load normally

### Profile Tests
- [ ] Can switch between profiles
- [ ] Kids mode blocks more content
- [ ] Adult mode allows more content
- [ ] Time limits work (if enabled)

---

## 🐛 Troubleshooting

### AI Service Won't Start
```bash
# Check if model exists
ls -lh ai-service/models/nsfw_model.onnx

# If missing, download:
wget https://github.com/bhky/opennsfw2/releases/download/v0.10.0/nsfw_model.onnx \
  -P ai-service/models/
```

### Chromium Build Fails
```bash
# Check disk space
df -h

# Check RAM
free -h

# Update depot_tools
cd ~/depot_tools
git pull
```

### Extension Not Loading
1. Check manifest.json is valid
2. Check console for errors (F12)
3. Reload extension in chrome://extensions/

---

## 📚 Next Steps

1. **Customize Profiles**: Edit JSON files in `profiles/`
2. **Add Blocklist Domains**: Edit `filters/url_blocklist.json`
3. **Adjust AI Threshold**: Modify threshold in extension settings
4. **Add Islamic Content**: Integrate Quran, Prayer times, etc.

---

## 🆘 Getting Help

- **Documentation**: See `docs/` folder
- **Issues**: GitHub Issues
- **Email**: support@halalbrowser.org
- **Community**: GitHub Discussions

---

## 🎯 Development Workflow

### Daily Development
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Start AI service
./scripts/start_ai_service.sh

# 3. Make changes to code

# 4. Test changes
python3 -m pytest tests/

# 5. Rebuild Chromium (if needed)
cd chromium-core/src
ninja -C out/Default chrome
```

### Adding New Features
1. Create feature branch
2. Implement feature
3. Add tests
4. Update documentation
5. Submit pull request

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Setup environment | 30 min |
| Download Chromium source | 1-2 hours |
| Build Chromium (first time) | 2-4 hours |
| Build Chromium (incremental) | 5-15 min |
| Test AI service | 5 min |
| Install extension | 2 min |

---

## 🌟 Tips for Success

1. **Use SSD**: Chromium build is I/O intensive
2. **More RAM = Faster**: 32GB recommended
3. **Parallel Build**: Use `-j$(nproc)` for ninja
4. **Incremental Builds**: Only rebuild changed files
5. **Cache Results**: AI service caches decisions

---

**May Allah bless your development journey!**

**الحمد لله رب العالمين**
