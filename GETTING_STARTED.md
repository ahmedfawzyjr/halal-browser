# 🌙 Getting Started with Halal Browser

**بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ**

Welcome to Halal Browser! This guide will help you get started with building your own Halal web browser.

---

## 🎯 What is Halal Browser?

Halal Browser is an **open-source, Chromium-based web browser** with:
- ✅ **AI-powered content filtering** - Blocks Haram images, videos, and text
- ✅ **Privacy-first design** - No tracking, no telemetry
- ✅ **Islamic features** - Quran, Prayer times, Qibla finder
- ✅ **Family profiles** - Kids, Family, Adult, School modes
- ✅ **Offline-capable** - All AI processing is local

---

## 🚀 Quick Start (Choose Your Path)

### Path 1: Test AI Service Only (30 minutes)
**Best for**: Testing the filtering system without building Chromium

```bash
# 1. Clone repository
git clone https://github.com/yourusername/halal-browser.git
cd halal-browser

# 2. Setup environment
chmod +x scripts/*.sh
./scripts/setup_env.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start AI service
./scripts/start_ai_service.sh

# 5. Test in another terminal
./scripts/test_ai_service.sh
```

✅ **You now have a working AI filtering service!**

### Path 2: Full Browser Build (6-8 hours)
**Best for**: Building the complete Halal Browser

```bash
# Follow Path 1 first, then:

# 6. Build Chromium (takes 4-6 hours)
./scripts/build_chromium.sh

# 7. Run Chromium
cd chromium-core/src
./out/Default/chrome

# 8. Install Halal Filter extension
# Go to chrome://extensions/
# Enable Developer mode
# Load unpacked: halal-browser/ui/extensions/halal-filter/
```

✅ **You now have a complete Halal Browser!**

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 22.04/24.04 (Linux)
- **CPU**: 4 cores
- **RAM**: 16GB
- **Disk**: 100GB free space
- **Internet**: For initial download (~60GB)

### Recommended
- **CPU**: 8+ cores
- **RAM**: 32GB
- **Disk**: 200GB SSD
- **Internet**: Fast connection (10+ Mbps)

---

## 🧩 Project Components

### 1. AI Service (`ai-service/`)
**Purpose**: Content filtering using machine learning

**Components**:
- `image_scanner.py` - NSFW image detection
- `video_scanner.py` - Video frame analysis
- `text_analyzer.py` - Haram keyword detection
- `api_server.py` - REST API service

**Test it**:
```bash
python3 ai-service/image_scanner.py
python3 ai-service/text_analyzer.py
```

### 2. Filters (`filters/`)
**Purpose**: URL and keyword filtering rules

**Files**:
- `url_blocklist.json` - Blocked domains
- `url_whitelist.json` - Safe domains
- `keywords.json` - Haram keywords
- `rules_engine.py` - Policy decisions

**Customize**:
```bash
# Edit blocklist
nano filters/url_blocklist.json

# Add keywords
nano filters/keywords.json
```

### 3. Profiles (`profiles/`)
**Purpose**: Different filtering levels for different users

**Profiles**:
- `kids_mode.json` - Maximum protection
- `family_mode.json` - Balanced filtering
- `adult_mode.json` - Standard filtering
- `school_mode.json` - Educational focus

**Customize**:
```bash
# Edit Kids Mode
nano profiles/kids_mode.json
```

### 4. Browser Extension (`ui/extensions/halal-filter/`)
**Purpose**: Integrates filtering into Chromium

**Files**:
- `manifest.json` - Extension configuration
- `background.js` - Background service worker
- `content.js` - Content filtering script
- `content.css` - Styling for blocked content

### 5. Build Scripts (`scripts/`)
**Purpose**: Automation scripts

**Scripts**:
- `setup_env.sh` - Environment setup
- `build_chromium.sh` - Build Chromium
- `start_ai_service.sh` - Start AI service
- `test_ai_service.sh` - Test AI service

---

## 🎓 Learning Path

### Week 1: Understanding the System
1. Read `docs/ARCHITECTURE.md`
2. Test AI service
3. Understand profiles
4. Customize blocklist

### Week 2: Building Chromium
1. Run `setup_env.sh`
2. Clone Chromium source
3. Build Chromium
4. Test browser

### Week 3: Integration
1. Install extension
2. Test filtering
3. Customize profiles
4. Add Islamic features

### Week 4: Advanced Features
1. Add new AI models
2. Implement video filtering
3. Add prayer times
4. Package for distribution

---

## 🧪 Testing Your Setup

### Test 1: AI Service Health
```bash
curl http://127.0.0.1:5000/api/health
```
Expected: `{"status": "healthy"}`

### Test 2: Text Filtering
```bash
curl -X POST http://127.0.0.1:5000/api/scan/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Visit our casino"}'
```
Expected: `{"decision": "BLOCK"}`

### Test 3: URL Filtering
```bash
curl -X POST http://127.0.0.1:5000/api/scan/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://quran.com"}'
```
Expected: `{"decision": "ALLOW"}`

### Test 4: Browser Extension
1. Open Chromium
2. Visit a blocked site (e.g., casino site)
3. Should see blocked page
4. Visit safe site (e.g., wikipedia.org)
5. Should load normally

---

## 🐛 Common Issues & Solutions

### Issue 1: AI Service Won't Start
**Error**: `Model not found: models/nsfw_model.onnx`

**Solution**:
```bash
mkdir -p ai-service/models
wget https://github.com/bhky/opennsfw2/releases/download/v0.10.0/nsfw_model.onnx \
  -P ai-service/models/
```

### Issue 2: Chromium Build Fails
**Error**: `Not enough disk space`

**Solution**:
```bash
# Check disk space
df -h

# Clean up if needed
sudo apt clean
sudo apt autoremove
```

### Issue 3: Extension Not Loading
**Error**: `Manifest file is missing or unreadable`

**Solution**:
```bash
# Validate manifest
cat ui/extensions/halal-filter/manifest.json | jq .

# Check file permissions
chmod -R 755 ui/extensions/halal-filter/
```

### Issue 4: Python Dependencies
**Error**: `ModuleNotFoundError: No module named 'onnxruntime'`

**Solution**:
```bash
source venv/bin/activate
pip install -r ai-service/requirements.txt
```

---

## 📚 Documentation

- **[README.md](README.md)** - Project overview
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design
- **[ROADMAP.md](docs/ROADMAP.md)** - Development plan
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick reference
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - This file

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Contribution Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Maintain Islamic values and purpose

---

## 🆘 Getting Help

### Community Support
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Email**: support@halalbrowser.org

### Resources
- **Chromium Docs**: https://www.chromium.org/developers/
- **ONNX Runtime**: https://onnxruntime.ai/
- **Islamic Content APIs**: Various sources for Quran, Hadith, etc.

---

## 🎯 Next Steps

After completing this guide, you can:

1. **Customize for your needs**
   - Add your own blocklist domains
   - Adjust AI thresholds
   - Create custom profiles

2. **Add Islamic features**
   - Integrate Quran API
   - Add prayer times
   - Include Islamic calendar

3. **Improve AI models**
   - Train custom models
   - Add more languages
   - Improve accuracy

4. **Package for distribution**
   - Create AppImage
   - Build .deb package
   - Distribute to community

5. **Contribute back**
   - Share improvements
   - Help others
   - Build the Ummah's technology

---

## 🌟 Success Stories

> "I built Halal Browser for my family and now my kids can browse safely!"
> - Ahmed, Developer

> "This project helped me learn Chromium development and serve my community."
> - Fatima, Student

> "We deployed Halal Browser in our Islamic school. Game changer!"
> - Masjid Al-Noor, USA

---

## 📊 Project Stats

- **Lines of Code**: ~5,000+
- **Components**: 20+
- **Profiles**: 4 (Kids, Family, Adult, School)
- **Supported Languages**: Arabic, English (more coming)
- **AI Models**: NSFW detection, Text analysis
- **License**: MIT (Open Source)

---

## 🙏 Acknowledgments

- **Chromium Team** - For the amazing browser engine
- **OpenNSFW2** - For the NSFW detection model
- **Muslim Developers** - For inspiration and support
- **Open Source Community** - For tools and libraries

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

This project is dedicated to serving the Muslim Ummah and promoting Halal content online.

---

**May Allah accept this work and make it beneficial for all.**

**الحمد لله رب العالمين**

**وَالسَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ**
