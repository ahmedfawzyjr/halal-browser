# 🌙 Halal Browser

**متصفح ويب إسلامي كامل مبني على Chromium مع حماية شاملة من المحتوى الحرام**

## 🎯 الهدف

بناء متصفح ويب:
- ✅ **Halal Content Only** - فلترة ذكية للمحتوى الحرام
- 🔒 **Privacy First** - حماية كاملة للخصوصية
- 🤖 **AI-Powered** - كشف تلقائي للمحتوى غير المناسب
- 🕌 **Islamic Features** - محتوى إسلامي متكامل
- 👨‍👩‍👧‍👦 **Family Safe** - أوضاع متعددة للعائلة والأطفال

## 📁 Project Structure

```
halal-browser/
├── chromium-core/          # Chromium source & build
├── ai-service/             # AI content filtering service
│   ├── models/             # ONNX/TFLite models
│   ├── image_scanner.py    # Image NSFW detection
│   ├── video_scanner.py    # Video frame analysis
│   ├── text_analyzer.py    # Text content analysis
│   └── api_server.py       # Local API service
├── filters/                # Content filtering rules
│   ├── url_blocklist.json  # Blocked domains
│   ├── url_whitelist.json  # Safe domains
│   ├── keywords.json       # Haram keywords
│   └── rules_engine.py     # Policy decision engine
├── profiles/               # User profiles & modes
│   ├── kids_mode.json      # Kids profile
│   ├── family_mode.json    # Family profile
│   ├── adult_mode.json     # Adult profile
│   └── school_mode.json    # School/Masjid profile
├── islamic-content/        # Islamic features
│   ├── quran/              # Quran + Tafsir
│   ├── hadith/             # Hadith database
│   ├── prayer_times/       # Prayer times calculator
│   └── qibla/              # Qibla finder
├── ui/                     # Browser UI customization
│   ├── themes/             # Islamic themes
│   ├── icons/              # Halal icon set
│   └── extensions/         # Built-in extensions
├── app-store/              # Halal apps ecosystem
│   ├── catalog.json        # App catalog
│   └── installer.py        # App installer
├── scripts/                # Build & deployment scripts
│   ├── setup_env.sh        # Environment setup
│   ├── build_chromium.sh   # Chromium build script
│   ├── install_deps.sh     # Dependencies installer
│   └── package.sh          # Packaging script
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md     # System architecture
│   ├── ROADMAP.md          # Development roadmap
│   ├── API.md              # API documentation
│   └── CONTRIBUTING.md     # Contribution guide
└── tests/                  # Testing suite
    ├── test_ai_filter.py   # AI filtering tests
    ├── test_profiles.py    # Profile tests
    └── test_integration.py # Integration tests
```

## 🚀 Quick Start

### Prerequisites
- Ubuntu 22.04/24.04 (recommended)
- 16GB+ RAM
- 100GB+ free disk space
- Python 3.10+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/halal-browser.git
cd halal-browser

# 2. Run setup script
./scripts/setup_env.sh

# 3. Build Chromium base
./scripts/build_chromium.sh

# 4. Install AI models
python3 ai-service/download_models.py

# 5. Run the browser
./chromium-core/out/Default/chrome
```

## 🧠 Core Features

### 1️⃣ Content Filtering
- **AI Image Detection** - NSFW/Haram image blocking
- **Video Analysis** - Frame-by-frame video scanning
- **Text Analysis** - Haram keyword detection
- **URL Filtering** - Domain blocklist/whitelist
- **Real-time Blurring** - Automatic content blurring

### 2️⃣ Privacy & Security
- **Forced SafeSearch** - All search engines
- **Tracker Blocker** - Anti-tracking protection
- **Ad Blocker** - Halal ads only
- **Encrypted Cache** - Local data encryption
- **No Telemetry** - Zero data collection

### 3️⃣ Profiles & Modes
- **Kids Mode** - Maximum protection, time limits
- **Family Mode** - Balanced filtering
- **Adult Mode** - Still blocks Haram content
- **School/Masjid Mode** - Educational focus

### 4️⃣ Islamic Content
- **Quran Reader** - Full Quran with Tafsir
- **Hadith Library** - Sahih collections
- **Prayer Times** - Automatic prayer notifications
- **Qibla Finder** - Built-in compass
- **Islamic Calendar** - Hijri calendar integration

### 5️⃣ AI Features
- **Offline AI** - All processing local
- **Smart Recommendations** - Halal content suggestions
- **Parental Reports** - Activity monitoring
- **Custom Rules** - Personalized filtering

## ⏱️ Development Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Phase 0** - Environment Setup | 1 week | Dev environment ready |
| **Phase 1** - Chromium Base | 2-3 weeks | Working Chromium build |
| **Phase 2** - AI Filtering | 4-6 weeks | Content filtering service |
| **Phase 3** - Integration | 2-3 weeks | AI + Browser integration |
| **Phase 4** - Profiles & Policy | 3-4 weeks | Profile system |
| **Phase 5** - Islamic Content | 2 weeks | Islamic features |
| **Phase 6** - App Store | 2 weeks | Halal apps ecosystem |
| **Phase 7** - UI/UX | 2 weeks | Arabic interface |
| **Phase 8** - Testing & Packaging | 2 weeks | Release packages |
| **Total MVP** | **4-5 months** | Halal Browser v1.0 |

## 🛠️ Tech Stack

- **Browser Core**: Chromium (C++)
- **AI Service**: Python + ONNX Runtime + TensorFlow Lite
- **Filtering**: OpenCV, NLP, Computer Vision
- **Policy Engine**: Python + JSON Rules
- **UI**: Qt/GTK (Arabic support)
- **Database**: SQLite
- **Packaging**: AppImage, .deb, Flatpak

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Development Roadmap](docs/ROADMAP.md)
- [API Documentation](docs/API.md)
- [Contributing Guide](docs/CONTRIBUTING.md)

## 🤝 Contributing

This is an open-source project. Contributions are welcome!

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

## 🌟 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/halal-browser/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/halal-browser/discussions)
- **Email**: support@halalbrowser.org

---

**Built with ❤️ for the Muslim Ummah**

الحمد لله رب العالمين
