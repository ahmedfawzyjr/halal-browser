"""
Rules Engine - Policy Decision Making
Determines whether content should be allowed, blurred, or blocked
"""

import json
import os
from datetime import datetime, time
from typing import Dict, List, Optional
from urllib.parse import urlparse


class RulesEngine:
    """
    Policy engine that makes decisions based on profiles and rules
    """
    
    def __init__(self, profile_manager, blocklist_path, whitelist_path):
        """
        Initialize rules engine
        
        Args:
            profile_manager: ProfileManager instance
            blocklist_path: Path to blocklist JSON
            whitelist_path: Path to whitelist JSON
        """
        self.profile_manager = profile_manager
        self.blocklist = self.load_list(blocklist_path)
        self.whitelist = self.load_list(whitelist_path)
        
        print("✅ Rules Engine initialized")
    
    def load_list(self, list_path: str) -> Dict:
        """Load blocklist or whitelist from JSON"""
        if not os.path.exists(list_path):
            print(f"⚠️  List not found: {list_path}")
            return {"categories": {}}
        
        try:
            with open(list_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading list: {e}")
            return {"categories": {}}
    
    def get_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain.lower()
        except:
            return url.lower()
    
    def is_domain_in_list(self, domain: str, domain_list: Dict) -> bool:
        """Check if domain is in blocklist/whitelist"""
        # Check all categories
        for category, domains in domain_list.get('categories', {}).items():
            for blocked_domain in domains:
                if blocked_domain in domain or domain in blocked_domain:
                    return True
        return False
    
    def check_time_limits(self, profile: Dict) -> Dict:
        """
        Check if current time is within allowed hours
        
        Returns:
            dict: {'allowed': bool, 'reason': str}
        """
        time_limits = profile.get('rules', {}).get('time_limits', {})
        
        if not time_limits.get('enabled'):
            return {'allowed': True, 'reason': 'No time limits'}
        
        # Check allowed hours
        allowed_hours = time_limits.get('allowed_hours')
        if allowed_hours:
            current_time = datetime.now().time()
            
            for time_range in allowed_hours:
                start_str, end_str = time_range.split('-')
                start_time = datetime.strptime(start_str, '%H:%M').time()
                end_time = datetime.strptime(end_str, '%H:%M').time()
                
                if start_time <= current_time <= end_time:
                    return {'allowed': True, 'reason': 'Within allowed hours'}
            
            return {
                'allowed': False,
                'reason': f'Outside allowed hours: {allowed_hours}'
            }
        
        return {'allowed': True, 'reason': 'No time restrictions'}
    
    def decide_url(self, url: str) -> Dict:
        """
        Decide whether URL should be allowed
        
        Args:
            url: URL to check
            
        Returns:
            dict: {
                'decision': str ('ALLOW', 'BLOCK', 'BLOCK_TIME'),
                'reason': str,
                'profile': str
            }
        """
        profile = self.profile_manager.get_active_profile()
        
        if not profile:
            return {
                'decision': 'ALLOW',
                'reason': 'No active profile',
                'profile': None
            }
        
        profile_name = profile.get('name', 'unknown')
        rules = profile.get('rules', {})
        
        # Check time limits
        time_check = self.check_time_limits(profile)
        if not time_check['allowed']:
            return {
                'decision': 'BLOCK_TIME',
                'reason': time_check['reason'],
                'profile': profile_name
            }
        
        # Extract domain
        domain = self.get_domain(url)
        
        # Check whitelist-only mode
        if rules.get('whitelist_only'):
            if self.is_domain_in_list(domain, self.whitelist):
                return {
                    'decision': 'ALLOW',
                    'reason': 'Domain in whitelist',
                    'profile': profile_name
                }
            else:
                return {
                    'decision': 'BLOCK',
                    'reason': 'Not in whitelist (whitelist-only mode)',
                    'profile': profile_name
                }
        
        # Check blocklist
        if self.is_domain_in_list(domain, self.blocklist):
            return {
                'decision': 'BLOCK',
                'reason': 'Domain in blocklist',
                'profile': profile_name
            }
        
        # Default allow
        return {
            'decision': 'ALLOW',
            'reason': 'Passed all checks',
            'profile': profile_name
        }
    
    def decide_content(self, content_type: str, ai_result: Dict) -> Dict:
        """
        Decide whether content should be allowed based on AI scan
        
        Args:
            content_type: 'image', 'video', or 'text'
            ai_result: AI scan result
            
        Returns:
            dict: {
                'decision': str ('ALLOW', 'BLUR', 'BLOCK'),
                'reason': str,
                'profile': str
            }
        """
        profile = self.profile_manager.get_active_profile()
        
        if not profile:
            return {
                'decision': 'ALLOW',
                'reason': 'No active profile',
                'profile': None
            }
        
        profile_name = profile.get('name', 'unknown')
        rules = profile.get('rules', {})
        
        # Check block all rules
        if content_type == 'image' and rules.get('block_all_images'):
            return {
                'decision': 'BLOCK',
                'reason': 'All images blocked by profile',
                'profile': profile_name
            }
        
        if content_type == 'video' and rules.get('block_all_videos'):
            return {
                'decision': 'BLOCK',
                'reason': 'All videos blocked by profile',
                'profile': profile_name
            }
        
        # Check AI result
        confidence = ai_result.get('confidence', 0)
        threshold = rules.get('nsfw_threshold', 0.7)
        
        if confidence > threshold:
            # Content exceeds threshold
            if rules.get('allow_blur') and content_type == 'image':
                return {
                    'decision': 'BLUR',
                    'reason': f'NSFW confidence {confidence:.2%} > threshold {threshold:.2%}',
                    'profile': profile_name
                }
            else:
                return {
                    'decision': 'BLOCK',
                    'reason': f'NSFW confidence {confidence:.2%} > threshold {threshold:.2%}',
                    'profile': profile_name
                }
        
        # Content is safe
        return {
            'decision': 'ALLOW',
            'reason': f'NSFW confidence {confidence:.2%} < threshold {threshold:.2%}',
            'profile': profile_name
        }
    
    def decide_download(self, file_url: str, file_type: str) -> Dict:
        """
        Decide whether download should be allowed
        
        Args:
            file_url: URL of file to download
            file_type: Type of file (e.g., 'exe', 'pdf', 'zip')
            
        Returns:
            Decision dict
        """
        profile = self.profile_manager.get_active_profile()
        
        if not profile:
            return {
                'decision': 'ALLOW',
                'reason': 'No active profile',
                'profile': None
            }
        
        profile_name = profile.get('name', 'unknown')
        rules = profile.get('rules', {})
        parental_controls = rules.get('parental_controls', {})
        
        # Check if downloads are blocked
        if parental_controls.get('block_downloads'):
            return {
                'decision': 'BLOCK',
                'reason': 'Downloads blocked by parental controls',
                'profile': profile_name
            }
        
        # Check URL
        url_decision = self.decide_url(file_url)
        if url_decision['decision'] != 'ALLOW':
            return url_decision
        
        return {
            'decision': 'ALLOW',
            'reason': 'Download allowed',
            'profile': profile_name
        }


class ProfileManager:
    """
    Manages user profiles and active profile selection
    """
    
    def __init__(self, profiles_dir: str):
        """
        Initialize profile manager
        
        Args:
            profiles_dir: Directory containing profile JSON files
        """
        self.profiles_dir = profiles_dir
        self.profiles = self.load_profiles()
        self.active_profile = None
        
        # Set default profile
        if 'family' in self.profiles:
            self.set_active_profile('family')
        elif self.profiles:
            self.set_active_profile(list(self.profiles.keys())[0])
        
        print(f"✅ Profile Manager initialized")
        print(f"   Loaded {len(self.profiles)} profiles")
        if self.active_profile:
            print(f"   Active profile: {self.active_profile['display_name']}")
    
    def load_profiles(self) -> Dict:
        """Load all profiles from directory"""
        profiles = {}
        
        if not os.path.exists(self.profiles_dir):
            print(f"⚠️  Profiles directory not found: {self.profiles_dir}")
            return profiles
        
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.profiles_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                        profile_name = profile.get('name')
                        if profile_name:
                            profiles[profile_name] = profile
                except Exception as e:
                    print(f"❌ Error loading profile {filename}: {e}")
        
        return profiles
    
    def get_profile(self, profile_name: str) -> Optional[Dict]:
        """Get profile by name"""
        return self.profiles.get(profile_name)
    
    def get_active_profile(self) -> Optional[Dict]:
        """Get currently active profile"""
        return self.active_profile
    
    def set_active_profile(self, profile_name: str) -> bool:
        """
        Set active profile
        
        Args:
            profile_name: Name of profile to activate
            
        Returns:
            True if successful, False otherwise
        """
        if profile_name in self.profiles:
            self.active_profile = self.profiles[profile_name]
            print(f"✅ Active profile set to: {self.active_profile['display_name']}")
            return True
        else:
            print(f"❌ Profile not found: {profile_name}")
            return False
    
    def list_profiles(self) -> List[Dict]:
        """Get list of all available profiles"""
        return [
            {
                'name': p['name'],
                'display_name': p['display_name'],
                'icon': p.get('icon', ''),
                'description': p.get('description', '')
            }
            for p in self.profiles.values()
        ]


def main():
    """Test the rules engine"""
    print("🧪 Testing Rules Engine...")
    
    # Initialize profile manager
    profile_manager = ProfileManager("../profiles")
    
    # Initialize rules engine
    rules_engine = RulesEngine(
        profile_manager,
        "../filters/url_blocklist.json",
        "../filters/url_whitelist.json"
    )
    
    # Test URLs
    test_urls = [
        "https://quran.com",
        "https://pornhub.com",
        "https://wikipedia.org",
        "https://bet365.com",
        "https://github.com"
    ]
    
    print("\n" + "="*60)
    print("Testing URL decisions:")
    print("="*60)
    
    for url in test_urls:
        decision = rules_engine.decide_url(url)
        print(f"\n🔍 URL: {url}")
        print(f"   Decision: {decision['decision']}")
        print(f"   Reason: {decision['reason']}")
        print(f"   Profile: {decision['profile']}")
    
    # Test content decisions
    print("\n" + "="*60)
    print("Testing content decisions:")
    print("="*60)
    
    test_ai_results = [
        {'confidence': 0.2, 'is_nsfw': False},
        {'confidence': 0.7, 'is_nsfw': True},
        {'confidence': 0.95, 'is_nsfw': True}
    ]
    
    for ai_result in test_ai_results:
        decision = rules_engine.decide_content('image', ai_result)
        print(f"\n🖼️  AI Result: confidence={ai_result['confidence']:.2%}")
        print(f"   Decision: {decision['decision']}")
        print(f"   Reason: {decision['reason']}")
    
    print("\n" + "="*60)
    print("✅ Testing completed")


if __name__ == "__main__":
    main()
