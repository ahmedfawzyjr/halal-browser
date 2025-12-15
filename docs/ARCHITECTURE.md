# 🏗️ Halal Browser - System Architecture

## Overview

Halal Browser is built on a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  (Browser UI, Settings, Islamic Content, Notifications)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Request Filter Layer                       │
│  (URL Filter, SafeSearch, Content Policy Enforcer)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      AI Service Layer                        │
│  (Image Scanner, Video Scanner, Text Analyzer)               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Policy Engine Layer                       │
│  (Profile Manager, Rules Engine, Decision Maker)             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Chromium Core Layer                        │
│  (Rendering Engine, Network Stack, Storage)                  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

**Purpose**: User interaction and display

**Components**:
- **Browser UI**: Custom Chromium UI with Islamic themes
- **Settings Panel**: Profile management, filter configuration
- **Islamic Widgets**: Quran reader, Prayer times, Qibla finder
- **Notification Center**: Prayer alerts, content warnings

**Technologies**:
- C++ (Chromium UI)
- HTML/CSS/JavaScript (Extensions)
- Qt/GTK (Native widgets)

**Key Files**:
- `ui/themes/`
- `ui/icons/`
- `ui/extensions/`

---

### 2. Request Filter Layer

**Purpose**: First-line content filtering before rendering

**Flow**:
```
User Request → URL Check → SafeSearch Injection → Content Policy → Render/Block
```

**Components**:

#### URL Filter
- Checks against blocklist/whitelist
- Domain reputation scoring
- Redirect blocking

#### SafeSearch Enforcer
- Forces SafeSearch on all search engines
- Google: `&safe=active`
- Bing: `&adlt=strict`
- DuckDuckGo: `&kp=1`

#### Content Policy Enforcer
- Applies profile-specific rules
- Decides: Allow / Blur / Block
- Logs decisions for parental reports

**Key Files**:
- `filters/url_blocklist.json`
- `filters/url_whitelist.json`
- `filters/rules_engine.py`

---

### 3. AI Service Layer

**Purpose**: Deep content analysis using machine learning

**Architecture**:
```
┌──────────────────────────────────────────────────────┐
│                   AI Service API                      │
│              (Local REST API on port 5000)            │
└──────────────────────────────────────────────────────┘
           ↓                ↓                ↓
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Image   │    │  Video   │    │   Text   │
    │ Scanner  │    │ Scanner  │    │ Analyzer │
    └──────────┘    └──────────┘    └──────────┘
           ↓                ↓                ↓
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  ONNX    │    │  Frame   │    │   NLP    │
    │  Model   │    │ Extractor│    │  Model   │
    └──────────┘    └──────────┘    └──────────┘
```

#### Image Scanner
**Model**: OpenNSFW2 (ONNX format)
**Input**: Image URL or Base64
**Output**: 
```json
{
  "is_nsfw": false,
  "confidence": 0.95,
  "categories": {
    "safe": 0.95,
    "suggestive": 0.03,
    "explicit": 0.02
  },
  "decision": "ALLOW"
}
```

**Process**:
1. Download/load image
2. Preprocess (resize, normalize)
3. Run through ONNX model
4. Apply threshold (default: 0.7)
5. Return decision

#### Video Scanner
**Approach**: Frame sampling + batch analysis
**Input**: Video URL
**Output**:
```json
{
  "is_safe": true,
  "frames_analyzed": 30,
  "unsafe_frames": 0,
  "decision": "ALLOW"
}
```

**Process**:
1. Extract frames (1 frame/second)
2. Batch process through Image Scanner
3. If any frame > threshold → Block entire video
4. Cache results for performance

#### Text Analyzer
**Model**: Custom NLP + Keyword matching
**Input**: Text content
**Output**:
```json
{
  "is_halal": true,
  "detected_keywords": [],
  "language": "ar",
  "decision": "ALLOW"
}
```

**Process**:
1. Language detection
2. Keyword matching (Haram words)
3. Context analysis (NLP)
4. Sentiment analysis
5. Return decision

**Key Files**:
- `ai-service/models/` - AI models
- `ai-service/image_scanner.py`
- `ai-service/video_scanner.py`
- `ai-service/text_analyzer.py`
- `ai-service/api_server.py`

**API Endpoints**:
```
POST /api/scan/image
POST /api/scan/video
POST /api/scan/text
GET  /api/health
```

---

### 4. Policy Engine Layer

**Purpose**: Decision-making based on profiles and rules

**Components**:

#### Profile Manager
Manages user profiles with different filtering levels:

**Kids Mode**:
```json
{
  "name": "kids",
  "age_range": "0-12",
  "rules": {
    "block_all_images": false,
    "block_all_videos": true,
    "nsfw_threshold": 0.3,
    "time_limits": {
      "daily_minutes": 60,
      "allowed_hours": ["14:00-17:00"]
    },
    "whitelist_only": true,
    "parental_reports": true
  }
}
```

**Family Mode**:
```json
{
  "name": "family",
  "age_range": "13+",
  "rules": {
    "block_all_images": false,
    "block_all_videos": false,
    "nsfw_threshold": 0.6,
    "time_limits": null,
    "whitelist_only": false,
    "parental_reports": true
  }
}
```

**Adult Mode**:
```json
{
  "name": "adult",
  "age_range": "18+",
  "rules": {
    "block_all_images": false,
    "block_all_videos": false,
    "nsfw_threshold": 0.8,
    "time_limits": null,
    "whitelist_only": false,
    "parental_reports": false
  }
}
```

**School/Masjid Mode**:
```json
{
  "name": "school",
  "age_range": "all",
  "rules": {
    "block_all_images": false,
    "block_all_videos": true,
    "nsfw_threshold": 0.4,
    "educational_only": true,
    "whitelist_only": true,
    "allowed_categories": ["education", "islamic", "news"]
  }
}
```

#### Rules Engine
**Decision Logic**:
```python
def decide_content(url, content_type, ai_result, profile):
    # 1. Check URL blocklist
    if url in blocklist:
        return "BLOCK"
    
    # 2. Check whitelist (if whitelist_only mode)
    if profile.whitelist_only and url not in whitelist:
        return "BLOCK"
    
    # 3. Check AI result
    if content_type == "image":
        if ai_result.nsfw_score > profile.nsfw_threshold:
            return "BLUR" if profile.allow_blur else "BLOCK"
    
    # 4. Check time limits
    if profile.time_limits and not in_allowed_time():
        return "BLOCK"
    
    # 5. Default allow
    return "ALLOW"
```

**Key Files**:
- `profiles/*.json` - Profile configurations
- `filters/rules_engine.py` - Decision logic

---

### 5. Chromium Core Layer

**Purpose**: Browser rendering and networking

**Modifications**:
1. **Content Interceptor**: Hooks into network requests
2. **Rendering Pipeline**: Injects blur/block overlays
3. **Extension API**: Custom APIs for Halal features
4. **Storage**: Encrypted local storage

**Integration Points**:
```cpp
// chromium-core/content/browser/halal_content_filter.cc

class HalalContentFilter {
public:
  // Called before loading any resource
  FilterDecision OnBeforeRequest(const GURL& url, 
                                  ResourceType type);
  
  // Called after receiving response headers
  FilterDecision OnResponseStarted(const GURL& url,
                                    const HttpHeaders& headers);
  
  // Called when image/video is about to render
  FilterDecision OnBeforeRender(const GURL& url,
                                 const ContentData& data);
};
```

**Key Files**:
- `chromium-core/content/browser/halal_content_filter.cc`
- `chromium-core/chrome/browser/halal_browser_main.cc`

---

## Data Flow

### Example: Loading a Web Page with Images

```
1. User enters URL
   ↓
2. Request Filter Layer
   - Check URL blocklist → PASS
   - Inject SafeSearch → DONE
   ↓
3. Chromium loads HTML
   ↓
4. Parser finds <img> tags
   ↓
5. For each image:
   a. Request Filter checks URL → PASS
   b. Download image
   c. Send to AI Service → POST /api/scan/image
   d. AI returns: { "decision": "BLUR", "confidence": 0.85 }
   e. Policy Engine checks profile → Kids Mode → BLOCK
   f. Chromium blocks image, shows placeholder
   ↓
6. Page renders with filtered content
   ↓
7. Log decision to parental report
```

---

## Performance Considerations

### 1. Caching
- **AI Results Cache**: Cache AI decisions for 24 hours
- **URL Reputation Cache**: Cache URL checks for 1 hour
- **Model Cache**: Keep models in memory

### 2. Batch Processing
- Process multiple images in parallel
- Batch video frames for efficiency

### 3. Lazy Loading
- Only scan images in viewport
- Defer off-screen content

### 4. Offline Mode
- All AI processing is local
- No external API calls
- Works without internet (after initial setup)

---

## Security

### 1. Local-Only AI
- All AI models run locally
- No data sent to external servers
- Privacy-first design

### 2. Encrypted Storage
- User profiles encrypted
- Browsing history encrypted
- Cache encrypted

### 3. Sandboxing
- AI service runs in separate process
- Limited file system access
- No network access for AI service

---

## Scalability

### 1. Model Updates
- Models can be updated independently
- Versioned model files
- Automatic fallback to previous version

### 2. Rule Updates
- JSON-based rules (easy to update)
- Community-contributed blocklists
- Automatic rule syncing (optional)

### 3. Plugin System
- Custom filters can be added
- Third-party AI models supported
- Extension API for developers

---

## Future Enhancements

1. **Cloud Sync** (Optional): Sync profiles across devices
2. **Community Reports**: Crowdsourced URL reporting
3. **Advanced AI**: Multi-modal models (text + image + context)
4. **Real-time Video**: Real-time video filtering (GPU-accelerated)
5. **Mobile Version**: Android/iOS ports

---

**Next**: See [ROADMAP.md](ROADMAP.md) for implementation plan.
