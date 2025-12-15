# 📥 Halal Browser - Installation Guide

**Complete installation instructions for all platforms**

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Ubuntu 22.04/24.04, Debian 11+, or similar Linux
- **CPU**: 4 cores (x86_64)
- **RAM**: 16GB
- **Disk**: 100GB free space
- **Internet**: For initial download (~60GB)

### Recommended
- **CPU**: 8+ cores
- **RAM**: 32GB
- **Disk**: 200GB SSD
- **Internet**: 10+ Mbps

---

## 🚀 Installation Methods

### Method 1: Quick Test (AI Service Only) - 30 minutes

**Best for**: Testing filtering without building Chromium

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv

# 2. Clone repository
git clone https://github.com/yourusername/halal-browser.git
cd halal-browser

# 3. Run setup
chmod +x scripts/*.sh
./scripts/setup_env.sh

# 4. Activate virtual environment
source venv/bin/activate

# 5. Start AI service
./scripts/start_ai_service.sh
```

**Test it**:
```bash
# In another terminal
./scripts/test_ai_service.sh
```

---

### Method 2: Full Browser Build - 6-8 hours

**Best for**: Complete Halal Browser with Chromium

#### Step 1: System Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install build tools
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
```

#### Step 2: Install Chromium Dependencies
```bash
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
```

#### Step 3: Clone and Setup
```bash
# Clone repository
git clone https://github.com/yourusername/halal-browser.git
cd halal-browser

# Run automated setup
chmod +x scripts/*.sh
./scripts/setup_env.sh
```

This will:
- ✅ Install depot_tools
- ✅ Create Python virtual environment
- ✅ Download AI models
- ✅ Set up project structure

#### Step 4: Build Chromium
```bash
# This takes 4-6 hours on first build
./scripts/build_chromium.sh
```

**What happens**:
1. Clones Chromium source (~20GB download)
2. Syncs dependencies (~40GB total)
3. Configures build
4. Builds Chromium (2-4 hours compile time)

#### Step 5: Install Extension
```bash
# Start Chromium
cd chromium-core/src
./out/Default/chrome

# In browser:
# 1. Go to chrome://extensions/
# 2. Enable "Developer mode"
# 3. Click "Load unpacked"
# 4. Select: halal-browser/ui/extensions/halal-filter/
```

#### Step 6: Start AI Service
```bash
# In a separate terminal
cd halal-browser
source venv/bin/activate
./scripts/start_ai_service.sh
```

---

### Method 3: Pre-built Package (Coming Soon)

```bash
# Download AppImage
wget https://github.com/yourusername/halal-browser/releases/download/v1.0.0/HalalBrowser-x86_64.AppImage

# Make executable
chmod +x HalalBrowser-x86_64.AppImage

# Run
./HalalBrowser-x86_64.AppImage
```

Or install .deb package:
```bash
# Download
wget https://github.com/yourusername/halal-browser/releases/download/v1.0.0/halal-browser_1.0.0_amd64.deb

# Install
sudo dpkg -i halal-browser_1.0.0_amd64.deb
sudo apt install -f  # Fix dependencies

# Run
halal-browser
```

---

## 🔧 Post-Installation Setup

### 1. Configure Profile
```bash
# Edit active profile
nano profiles/family_mode.json

# Or use Kids Mode
# Edit: profiles/kids_mode.json
```

### 2. Customize Blocklist
```bash
# Add blocked domains
nano filters/url_blocklist.json

# Add safe domains
nano filters/url_whitelist.json
```

### 3. Add Keywords
```bash
# Edit Haram keywords
nano filters/keywords.json
```

### 4. Test Filtering
Visit these sites to test:
- ✅ https://wikipedia.org (should load)
- ✅ https://quran.com (should load)
- 🛑 Casino sites (should block)

---

## 🧪 Verification

### Check AI Service
```bash
curl http://127.0.0.1:5000/api/health
```
Expected: `{"status": "healthy"}`

### Check Extension
1. Open browser
2. Go to `chrome://extensions/`
3. Verify "Halal Content Filter" is enabled

### Check Filtering
```bash
# Test text filtering
curl -X POST http://127.0.0.1:5000/api/scan/text \
  -H "Content-Type: application/json" \
  -d '{"text": "casino gambling"}'
```
Expected: `{"decision": "BLOCK"}`

---

## 🐛 Troubleshooting

### Issue: AI Model Not Found
```bash
# Download model manually
mkdir -p ai-service/models
wget https://github.com/bhky/opennsfw2/releases/download/v0.10.0/nsfw_model.onnx \
  -P ai-service/models/
```

### Issue: Chromium Build Fails
```bash
# Check disk space (need 100GB+)
df -h

# Check RAM (need 16GB+)
free -h

# Clean and retry
cd chromium-core/src
rm -rf out/
./scripts/build_chromium.sh
```

### Issue: Python Dependencies
```bash
# Reinstall dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r ai-service/requirements.txt
```

### Issue: Extension Not Loading
```bash
# Check manifest
cat ui/extensions/halal-filter/manifest.json | python3 -m json.tool

# Fix permissions
chmod -R 755 ui/extensions/halal-filter/
```

### Issue: Port 5000 Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill it
sudo kill -9 <PID>

# Or change port in api_server.py
nano ai-service/api_server.py
# Change: app.run(port=5001)
```

---

## 📊 Installation Time Estimates

| Step | Time |
|------|------|
| System dependencies | 10 min |
| Clone repository | 2 min |
| Setup environment | 15 min |
| Download Chromium source | 1-2 hours |
| Build Chromium | 2-4 hours |
| Install extension | 2 min |
| **Total** | **4-7 hours** |

---

## 💾 Disk Space Breakdown

| Component | Size |
|-----------|------|
| Chromium source | ~20GB |
| Chromium dependencies | ~20GB |
| Chromium build output | ~15GB |
| AI models | ~50MB |
| Python dependencies | ~500MB |
| Project files | ~100MB |
| **Total** | **~55GB** |

---

## 🔄 Updating

### Update AI Service
```bash
cd halal-browser
git pull
source venv/bin/activate
pip install -r ai-service/requirements.txt --upgrade
```

### Update Chromium
```bash
cd chromium-core/src
git pull origin main
gclient sync
ninja -C out/Default chrome
```

### Update Extension
```bash
cd halal-browser
git pull
# Reload extension in chrome://extensions/
```

---

## 🗑️ Uninstallation

### Remove Halal Browser
```bash
# Stop AI service
pkill -f api_server.py

# Remove project
rm -rf ~/halal-browser

# Remove depot_tools (optional)
rm -rf ~/depot_tools

# Remove from PATH
nano ~/.bashrc
# Remove line: export PATH="$HOME/depot_tools:$PATH"
```

### Remove System Packages
```bash
# Only if not needed for other projects
sudo apt remove --purge \
  build-essential \
  clang \
  cmake \
  ninja-build
sudo apt autoremove
```

---

## 🆘 Getting Help

### Before Asking for Help
1. Check this installation guide
2. Read [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
3. Search [GitHub Issues](https://github.com/yourusername/halal-browser/issues)

### Report an Issue
1. Go to GitHub Issues
2. Click "New Issue"
3. Provide:
   - OS version: `lsb_release -a`
   - Error messages
   - Steps to reproduce

### Community Support
- **GitHub Discussions**: Ask questions
- **Email**: support@halalbrowser.org
- **Documentation**: See `docs/` folder

---

## ✅ Installation Checklist

- [ ] System meets minimum requirements
- [ ] All dependencies installed
- [ ] Repository cloned
- [ ] Setup script completed
- [ ] Virtual environment activated
- [ ] AI models downloaded
- [ ] Chromium built successfully
- [ ] Extension installed
- [ ] AI service running
- [ ] Filtering tested and working

---

## 🎯 Next Steps

After installation:
1. **Read**: [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Customize**: Edit profiles and filters
3. **Test**: Browse safe and blocked sites
4. **Configure**: Adjust settings for your needs
5. **Contribute**: Help improve the project

---

**May Allah make this installation easy for you!**

**الحمد لله رب العالمين**
