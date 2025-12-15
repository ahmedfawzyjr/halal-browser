"""
Text Analyzer - Haram Content Detection in Text
Detects inappropriate keywords and content in text
"""

import re
import json
import os
from typing import List, Dict, Set


class TextAnalyzer:
    """
    Text content analyzer for detecting Haram keywords and phrases
    Supports multiple languages (Arabic, English, etc.)
    """
    
    def __init__(self, keywords_path="filters/keywords.json"):
        """
        Initialize text analyzer
        
        Args:
            keywords_path: Path to keywords JSON file
        """
        self.keywords_path = keywords_path
        self.haram_keywords = self.load_keywords()
        
        # Compile regex patterns for faster matching
        self.patterns = self._compile_patterns()
        
        print(f"✅ Text Analyzer initialized")
        print(f"   Loaded {len(self.haram_keywords.get('en', []))} English keywords")
        print(f"   Loaded {len(self.haram_keywords.get('ar', []))} Arabic keywords")
    
    def load_keywords(self) -> Dict[str, List[str]]:
        """
        Load Haram keywords from JSON file
        
        Returns:
            Dictionary of keywords by language
        """
        if not os.path.exists(self.keywords_path):
            print(f"⚠️  Keywords file not found: {self.keywords_path}")
            print("   Using default keywords")
            return self._get_default_keywords()
        
        try:
            with open(self.keywords_path, 'r', encoding='utf-8') as f:
                keywords = json.load(f)
            return keywords
        except Exception as e:
            print(f"❌ Error loading keywords: {e}")
            return self._get_default_keywords()
    
    def _get_default_keywords(self) -> Dict[str, List[str]]:
        """Get default Haram keywords"""
        return {
            "en": [
                "porn", "xxx", "adult", "nsfw", "sex", "nude", "naked",
                "gambling", "casino", "betting", "poker", "slots",
                "alcohol", "beer", "wine", "vodka", "whiskey",
                "drugs", "cocaine", "marijuana", "weed", "heroin"
            ],
            "ar": [
                "إباحي", "جنس", "عاري", "عارية",
                "قمار", "كازينو", "مراهنات", "رهان",
                "خمر", "كحول", "بيرة", "نبيذ",
                "مخدرات", "حشيش", "كوكايين"
            ]
        }
    
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """
        Compile regex patterns for all keywords
        
        Returns:
            Dictionary of compiled patterns by language
        """
        patterns = {}
        
        for lang, keywords in self.haram_keywords.items():
            patterns[lang] = []
            for keyword in keywords:
                # Word boundary pattern for exact matching
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                patterns[lang].append((keyword, pattern))
        
        return patterns
    
    def detect_language(self, text: str) -> str:
        """
        Detect text language (simple heuristic)
        
        Args:
            text: Input text
            
        Returns:
            Language code ('ar', 'en', etc.)
        """
        # Check for Arabic characters
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        total_chars = len(re.findall(r'[a-zA-Z\u0600-\u06FF]', text))
        
        if total_chars == 0:
            return 'en'
        
        arabic_ratio = arabic_chars / total_chars
        
        if arabic_ratio > 0.3:
            return 'ar'
        else:
            return 'en'
    
    def scan(self, text: str, check_all_languages: bool = True) -> Dict:
        """
        Scan text for Haram content
        
        Args:
            text: Text to analyze
            check_all_languages: Check all languages or just detected language
            
        Returns:
            dict: {
                'is_halal': bool,
                'detected_keywords': list,
                'language': str,
                'decision': str ('ALLOW', 'BLOCK')
            }
        """
        if not text or not text.strip():
            return {
                'is_halal': True,
                'detected_keywords': [],
                'language': 'unknown',
                'decision': 'ALLOW'
            }
        
        text_lower = text.lower()
        detected_keywords = []
        
        # Detect language
        detected_lang = self.detect_language(text)
        
        # Check patterns
        if check_all_languages:
            # Check all languages
            languages_to_check = self.patterns.keys()
        else:
            # Check only detected language
            languages_to_check = [detected_lang] if detected_lang in self.patterns else ['en']
        
        for lang in languages_to_check:
            if lang not in self.patterns:
                continue
            
            for keyword, pattern in self.patterns[lang]:
                if pattern.search(text_lower):
                    detected_keywords.append({
                        'keyword': keyword,
                        'language': lang
                    })
        
        # Determine result
        is_halal = len(detected_keywords) == 0
        decision = 'ALLOW' if is_halal else 'BLOCK'
        
        return {
            'is_halal': is_halal,
            'detected_keywords': detected_keywords,
            'language': detected_lang,
            'decision': decision
        }
    
    def scan_url(self, url: str) -> Dict:
        """
        Scan URL for Haram keywords
        
        Args:
            url: URL to check
            
        Returns:
            Scan result dict
        """
        return self.scan(url, check_all_languages=True)
    
    def add_keyword(self, keyword: str, language: str = 'en'):
        """
        Add a new Haram keyword
        
        Args:
            keyword: Keyword to add
            language: Language code
        """
        if language not in self.haram_keywords:
            self.haram_keywords[language] = []
        
        if keyword not in self.haram_keywords[language]:
            self.haram_keywords[language].append(keyword)
            
            # Recompile patterns
            self.patterns = self._compile_patterns()
            
            # Save to file
            self.save_keywords()
            
            print(f"✅ Added keyword: {keyword} ({language})")
    
    def remove_keyword(self, keyword: str, language: str = 'en'):
        """
        Remove a keyword
        
        Args:
            keyword: Keyword to remove
            language: Language code
        """
        if language in self.haram_keywords:
            if keyword in self.haram_keywords[language]:
                self.haram_keywords[language].remove(keyword)
                
                # Recompile patterns
                self.patterns = self._compile_patterns()
                
                # Save to file
                self.save_keywords()
                
                print(f"✅ Removed keyword: {keyword} ({language})")
    
    def save_keywords(self):
        """Save keywords to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.keywords_path), exist_ok=True)
            with open(self.keywords_path, 'w', encoding='utf-8') as f:
                json.dump(self.haram_keywords, f, ensure_ascii=False, indent=2)
            print(f"✅ Keywords saved to: {self.keywords_path}")
        except Exception as e:
            print(f"❌ Error saving keywords: {e}")


def main():
    """Test the text analyzer"""
    print("🧪 Testing Text Analyzer...")
    
    # Initialize analyzer
    analyzer = TextAnalyzer()
    
    # Test cases
    test_texts = [
        "This is a safe and halal text about education",
        "Visit our casino for gambling and poker",
        "هذا نص آمن عن التعليم الإسلامي",
        "موقع قمار ومراهنات",
        "Buy alcohol and drugs online",
        "Learn Quran and Islamic studies"
    ]
    
    print("\n" + "="*60)
    for i, text in enumerate(test_texts, 1):
        print(f"\n🔍 Test {i}: {text[:50]}...")
        result = analyzer.scan(text)
        print(f"   Decision: {result['decision']}")
        print(f"   Language: {result['language']}")
        print(f"   Is Halal: {result['is_halal']}")
        if result['detected_keywords']:
            print(f"   Detected: {result['detected_keywords']}")
    
    print("\n" + "="*60)
    print("✅ Testing completed")


if __name__ == "__main__":
    main()
