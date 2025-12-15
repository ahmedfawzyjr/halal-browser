"""
Image Scanner - NSFW Detection using ONNX Runtime
Detects inappropriate images using AI models
"""

import onnxruntime as ort
import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import hashlib
import json
import os


class ImageScanner:
    """
    AI-powered image scanner for NSFW content detection
    Uses ONNX models for fast, offline inference
    """
    
    def __init__(self, model_path, cache_dir="cache"):
        """
        Initialize the image scanner
        
        Args:
            model_path: Path to ONNX model file
            cache_dir: Directory for caching results
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Load ONNX model
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape
        
        # Cache setup
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        print(f"✅ Image Scanner initialized with model: {model_path}")
        print(f"   Input shape: {self.input_shape}")
    
    def preprocess(self, image):
        """
        Preprocess image for model input
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Preprocessed numpy array
        """
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model input size
        target_size = (self.input_shape[2], self.input_shape[3])
        image = image.resize(target_size, Image.BILINEAR)
        
        # Convert to numpy array
        img_array = np.array(image).astype(np.float32)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        # Transpose to (C, H, W)
        img_array = np.transpose(img_array, (2, 0, 1))
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def load_image(self, image_source):
        """
        Load image from file path or URL
        
        Args:
            image_source: File path or URL
            
        Returns:
            PIL Image
        """
        if image_source.startswith('http://') or image_source.startswith('https://'):
            # Download from URL
            response = requests.get(image_source, timeout=10)
            image = Image.open(BytesIO(response.content))
        else:
            # Load from file
            image = Image.open(image_source)
        
        return image
    
    def get_cache_key(self, image_source):
        """Generate cache key from image source"""
        return hashlib.md5(image_source.encode()).hexdigest()
    
    def get_cached_result(self, image_source):
        """
        Get cached scan result
        
        Args:
            image_source: Image path or URL
            
        Returns:
            Cached result dict or None
        """
        cache_key = self.get_cache_key(image_source)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        return None
    
    def cache_result(self, image_source, result):
        """
        Cache scan result
        
        Args:
            image_source: Image path or URL
            result: Scan result dict
        """
        cache_key = self.get_cache_key(image_source)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        with open(cache_file, 'w') as f:
            json.dump(result, f)
    
    def scan(self, image_source, threshold=0.7, use_cache=True):
        """
        Scan image for NSFW content
        
        Args:
            image_source: Image file path or URL
            threshold: NSFW threshold (0.0 - 1.0)
            use_cache: Whether to use cached results
            
        Returns:
            dict: {
                'is_nsfw': bool,
                'confidence': float,
                'categories': dict,
                'decision': str ('ALLOW', 'BLUR', 'BLOCK')
            }
        """
        # Check cache
        if use_cache:
            cached = self.get_cached_result(image_source)
            if cached:
                print(f"📦 Using cached result for: {image_source[:50]}...")
                return cached
        
        try:
            # Load and preprocess image
            image = self.load_image(image_source)
            img_array = self.preprocess(image)
            
            # Run inference
            outputs = self.session.run(None, {self.input_name: img_array})
            
            # Parse results (assuming binary classification: safe/nsfw)
            # Adjust based on your specific model output format
            if len(outputs[0][0]) == 2:
                # Binary classification
                safe_score = float(outputs[0][0][0])
                nsfw_score = float(outputs[0][0][1])
                
                categories = {
                    'safe': safe_score,
                    'nsfw': nsfw_score
                }
            else:
                # Multi-class classification
                scores = outputs[0][0]
                categories = {
                    'safe': float(scores[0]),
                    'suggestive': float(scores[1]) if len(scores) > 1 else 0.0,
                    'explicit': float(scores[2]) if len(scores) > 2 else 0.0
                }
                nsfw_score = max(categories['suggestive'], categories['explicit'])
            
            # Determine decision
            is_nsfw = nsfw_score > threshold
            
            if is_nsfw:
                if nsfw_score > 0.9:
                    decision = 'BLOCK'
                else:
                    decision = 'BLUR'
            else:
                decision = 'ALLOW'
            
            result = {
                'is_nsfw': is_nsfw,
                'confidence': nsfw_score,
                'categories': categories,
                'decision': decision,
                'threshold': threshold
            }
            
            # Cache result
            if use_cache:
                self.cache_result(image_source, result)
            
            return result
            
        except Exception as e:
            print(f"❌ Error scanning image: {e}")
            return {
                'is_nsfw': False,
                'confidence': 0.0,
                'categories': {},
                'decision': 'ALLOW',
                'error': str(e)
            }
    
    def scan_batch(self, image_sources, threshold=0.7, use_cache=True):
        """
        Scan multiple images in batch
        
        Args:
            image_sources: List of image paths or URLs
            threshold: NSFW threshold
            use_cache: Whether to use cached results
            
        Returns:
            List of scan results
        """
        results = []
        
        for image_source in image_sources:
            result = self.scan(image_source, threshold, use_cache)
            results.append(result)
        
        return results


def main():
    """Test the image scanner"""
    print("🧪 Testing Image Scanner...")
    
    # Initialize scanner
    model_path = "models/nsfw_model.onnx"
    
    if not os.path.exists(model_path):
        print(f"⚠️  Model not found: {model_path}")
        print("📥 Please download the model first:")
        print("   wget https://github.com/bhky/opennsfw2/releases/download/v0.10.0/nsfw_model.onnx -P models/")
        return
    
    scanner = ImageScanner(model_path)
    
    # Test with sample images
    test_images = [
        "tests/data/safe_image.jpg",
        "tests/data/test_image.jpg"
    ]
    
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\n🔍 Scanning: {image_path}")
            result = scanner.scan(image_path)
            print(f"   Result: {result['decision']}")
            print(f"   Confidence: {result['confidence']:.2%}")
            print(f"   Categories: {result['categories']}")
        else:
            print(f"⚠️  Image not found: {image_path}")


if __name__ == "__main__":
    main()
