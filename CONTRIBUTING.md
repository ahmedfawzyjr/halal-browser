# 🤝 Contributing to Halal Browser

**بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ**

Thank you for your interest in contributing to Halal Browser! This project is built for the Muslim Ummah, and every contribution is a form of Sadaqah Jariyah (ongoing charity).

---

## 🌟 Ways to Contribute

### 1. Code Contributions
- Fix bugs
- Add new features
- Improve performance
- Enhance AI models
- Add tests

### 2. Documentation
- Improve guides
- Translate to other languages
- Add tutorials
- Create video guides

### 3. Testing
- Test on different systems
- Report bugs
- Verify fixes
- Test new features

### 4. Design
- Create Islamic themes
- Design icons
- Improve UI/UX
- Create promotional materials

### 5. Islamic Content
- Review filtering criteria
- Suggest Islamic features
- Provide Halal/Haram guidance
- Validate Islamic content

### 6. Community
- Answer questions
- Help other users
- Share the project
- Organize events

---

## 🚀 Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/halal-browser.git
cd halal-browser
```

### 2. Set Up Development Environment
```bash
# Run setup script
./scripts/setup_env.sh

# Activate virtual environment
source venv/bin/activate
```

### 3. Create a Branch
```bash
# Create feature branch
git checkout -b feature/amazing-feature

# Or bug fix branch
git checkout -b fix/bug-description
```

### 4. Make Your Changes
```bash
# Edit files
nano ai-service/image_scanner.py

# Test your changes
python3 -m pytest tests/
```

### 5. Commit Your Changes
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add: Amazing feature that does X"
```

### 6. Push to GitHub
```bash
# Push to your fork
git push origin feature/amazing-feature
```

### 7. Create Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill in the template
4. Submit for review

---

## 📝 Commit Message Guidelines

### Format
```
Type: Brief description

Detailed explanation (optional)

Fixes #issue_number (if applicable)
```

### Types
- **Add**: New feature or file
- **Fix**: Bug fix
- **Update**: Update existing feature
- **Remove**: Remove code or file
- **Refactor**: Code restructuring
- **Docs**: Documentation changes
- **Test**: Add or update tests
- **Style**: Code style changes

### Examples
```bash
# Good commits
git commit -m "Add: Video frame extraction for NSFW detection"
git commit -m "Fix: Image scanner crashes on large images"
git commit -m "Update: Increase AI threshold for Kids Mode"
git commit -m "Docs: Add Arabic translation for README"

# Bad commits
git commit -m "fixed stuff"
git commit -m "update"
git commit -m "changes"
```

---

## 🧪 Testing Requirements

### Before Submitting PR
- [ ] All existing tests pass
- [ ] New tests added for new features
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No console errors

### Run Tests
```bash
# Run all tests
python3 -m pytest tests/

# Run specific test
python3 -m pytest tests/test_ai_filter.py

# Run with coverage
python3 -m pytest --cov=ai-service tests/
```

### Manual Testing
```bash
# Test AI service
./scripts/start_ai_service.sh
./scripts/test_ai_service.sh

# Test browser
cd chromium-core/src
./out/Default/chrome
```

---

## 📋 Code Style Guidelines

### Python Code
```python
# Use descriptive names
def scan_image_for_nsfw(image_path, threshold=0.7):
    """
    Scan image for NSFW content
    
    Args:
        image_path: Path to image file
        threshold: NSFW detection threshold (0.0-1.0)
        
    Returns:
        dict: Scan result with decision
    """
    pass

# Use type hints
def process_result(confidence: float) -> str:
    return "BLOCK" if confidence > 0.7 else "ALLOW"

# Use constants
NSFW_THRESHOLD = 0.7
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
```

### JavaScript Code
```javascript
// Use const/let, not var
const API_URL = 'http://127.0.0.1:5000';
let currentProfile = 'family';

// Use arrow functions
const scanImage = async (imageUrl) => {
  const result = await fetch(`${API_URL}/api/scan/image`, {
    method: 'POST',
    body: JSON.stringify({ image_url: imageUrl })
  });
  return result.json();
};

// Use descriptive names
function blockImageElement(imgElement) {
  imgElement.style.display = 'none';
}
```

### JSON Files
```json
{
  "name": "profile_name",
  "description": "Clear description",
  "rules": {
    "nsfw_threshold": 0.7,
    "block_all_videos": false
  }
}
```

---

## 🔍 Code Review Process

### What We Look For
1. **Functionality**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Documentation**: Is it well documented?
4. **Style**: Does it follow guidelines?
5. **Islamic Values**: Does it align with project mission?

### Review Timeline
- **Initial Review**: Within 48 hours
- **Follow-up**: Within 24 hours
- **Merge**: After approval from 2+ maintainers

### Feedback
- Be respectful and constructive
- Explain reasoning
- Suggest improvements
- Acknowledge good work

---

## 🎯 Priority Areas

### High Priority
- [ ] Improve AI accuracy
- [ ] Add more language support
- [ ] Optimize performance
- [ ] Fix critical bugs
- [ ] Security improvements

### Medium Priority
- [ ] Add Islamic features
- [ ] Improve UI/UX
- [ ] Add more profiles
- [ ] Enhance documentation
- [ ] Add more tests

### Low Priority
- [ ] Code refactoring
- [ ] Style improvements
- [ ] Minor optimizations

---

## 🌍 Translation Guidelines

### Adding New Language
1. Create language file: `filters/keywords_XX.json`
2. Translate keywords
3. Update `text_analyzer.py`
4. Add language detection
5. Test thoroughly

### Translation Quality
- Use native speakers
- Maintain Islamic terminology
- Keep technical accuracy
- Test with real content

---

## 🐛 Bug Report Guidelines

### Before Reporting
1. Search existing issues
2. Test on latest version
3. Reproduce consistently
4. Gather information

### Bug Report Template
```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Ubuntu 22.04
- Browser: Chromium 120.0
- Python: 3.10.12

**Screenshots**
If applicable

**Logs**
Relevant error messages
```

---

## 💡 Feature Request Guidelines

### Before Requesting
1. Check existing requests
2. Ensure it aligns with project goals
3. Consider Islamic values
4. Think about implementation

### Feature Request Template
```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this needed?

**Proposed Solution**
How should it work?

**Alternatives**
Other ways to achieve this

**Islamic Consideration**
How does this serve the Ummah?
```

---

## 🏆 Recognition

### Contributors
All contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation
- Remembered in our duas

### Top Contributors
Special recognition for:
- Most commits
- Best code quality
- Most helpful reviews
- Best documentation

---

## 📜 Code of Conduct

### Our Values
1. **Respect**: Treat everyone with respect
2. **Inclusivity**: Welcome all contributors
3. **Islamic Ethics**: Maintain Islamic values
4. **Professionalism**: Be professional
5. **Collaboration**: Work together

### Unacceptable Behavior
- Harassment or discrimination
- Offensive language
- Personal attacks
- Spam or trolling
- Violation of Islamic principles

### Reporting
Report violations to: conduct@halalbrowser.org

---

## 🎓 Learning Resources

### For New Contributors
- [Git Basics](https://git-scm.com/book/en/v2)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [Chromium Development](https://www.chromium.org/developers/)

### For Advanced Contributors
- [ONNX Runtime](https://onnxruntime.ai/docs/)
- [OpenCV](https://docs.opencv.org/)
- [Browser Extensions](https://developer.chrome.com/docs/extensions/)
- [AI/ML Basics](https://www.tensorflow.org/tutorials)

---

## 📞 Contact

### Maintainers
- **Lead Developer**: [Name] - email@example.com
- **AI/ML Lead**: [Name] - email@example.com
- **Islamic Advisor**: [Name] - email@example.com

### Community
- **GitHub Discussions**: Ask questions
- **Discord**: [Link] (Coming soon)
- **Email**: contribute@halalbrowser.org

---

## 🙏 Final Words

Every contribution, no matter how small, is valuable. Whether you fix a typo, report a bug, or add a major feature, you are helping protect Muslims online and earning reward from Allah.

**May Allah accept your contributions and make them a means of continuous reward.**

**جَزَاكَ اللَّهُ خَيْرًا**

**الحمد لله رب العالمين**

---

## ✅ Contribution Checklist

Before submitting your PR:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added (if applicable)
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] Islamic values maintained
- [ ] Ready for review

---

**Thank you for contributing to Halal Browser!**

**Together, we can make the internet a safer place for Muslims.**

**بارك الله فيك**
