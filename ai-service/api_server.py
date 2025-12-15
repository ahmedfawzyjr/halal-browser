"""
AI Service API Server
Local REST API for content filtering services
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Import scanners
from image_scanner import ImageScanner
from video_scanner import VideoScanner
from text_analyzer import TextAnalyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for browser extension

# Initialize scanners
print("🚀 Initializing AI Service...")

MODEL_PATH = "models/nsfw_model.onnx"
KEYWORDS_PATH = "../filters/keywords.json"

# Check if model exists
if not os.path.exists(MODEL_PATH):
    print(f"⚠️  Model not found: {MODEL_PATH}")
    print("📥 Please download the model:")
    print("   mkdir -p models")
    print("   wget https://github.com/bhky/opennsfw2/releases/download/v0.10.0/nsfw_model.onnx -P models/")
    sys.exit(1)

# Initialize services
image_scanner = ImageScanner(MODEL_PATH)
video_scanner = VideoScanner(image_scanner)
text_analyzer = TextAnalyzer(KEYWORDS_PATH)

print("✅ AI Service ready!")


@app.route('/')
def index():
    """API information"""
    return jsonify({
        'name': 'Halal Browser AI Service',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'scan_image': '/api/scan/image',
            'scan_video': '/api/scan/video',
            'scan_text': '/api/scan/text',
            'scan_url': '/api/scan/url'
        }
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'image_scanner': 'ready',
            'video_scanner': 'ready',
            'text_analyzer': 'ready'
        }
    })


@app.route('/api/scan/image', methods=['POST'])
def scan_image():
    """
    Scan image for NSFW content
    
    Request body:
    {
        "image_path": "path/to/image.jpg",  // or "image_url"
        "threshold": 0.7  // optional
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        image_source = data.get('image_path') or data.get('image_url')
        threshold = data.get('threshold', 0.7)
        
        if not image_source:
            return jsonify({'error': 'image_path or image_url required'}), 400
        
        # Validate threshold
        if not 0 <= threshold <= 1:
            return jsonify({'error': 'threshold must be between 0 and 1'}), 400
        
        # Scan image
        result = image_scanner.scan(image_source, threshold)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/video', methods=['POST'])
def scan_video():
    """
    Scan video for NSFW content
    
    Request body:
    {
        "video_path": "path/to/video.mp4",  // or "video_url"
        "threshold": 0.7,  // optional
        "fps": 1,  // optional, frames per second to extract
        "max_frames": 30  // optional, maximum frames to analyze
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_source = data.get('video_path') or data.get('video_url')
        threshold = data.get('threshold', 0.7)
        fps = data.get('fps', 1)
        max_frames = data.get('max_frames', 30)
        
        if not video_source:
            return jsonify({'error': 'video_path or video_url required'}), 400
        
        # Validate parameters
        if not 0 <= threshold <= 1:
            return jsonify({'error': 'threshold must be between 0 and 1'}), 400
        
        if fps <= 0 or fps > 30:
            return jsonify({'error': 'fps must be between 1 and 30'}), 400
        
        if max_frames <= 0 or max_frames > 100:
            return jsonify({'error': 'max_frames must be between 1 and 100'}), 400
        
        # Scan video
        if video_source.startswith('http://') or video_source.startswith('https://'):
            result = video_scanner.scan_url(video_source, threshold, fps, max_frames)
        else:
            result = video_scanner.scan(video_source, threshold, fps, max_frames)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/text', methods=['POST'])
def scan_text():
    """
    Scan text for Haram keywords
    
    Request body:
    {
        "text": "text to analyze"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        text = data.get('text')
        
        if not text:
            return jsonify({'error': 'text required'}), 400
        
        # Scan text
        result = text_analyzer.scan(text)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/url', methods=['POST'])
def scan_url():
    """
    Scan URL for Haram keywords
    
    Request body:
    {
        "url": "https://example.com"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'url required'}), 400
        
        # Scan URL
        result = text_analyzer.scan_url(url)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/keywords/add', methods=['POST'])
def add_keyword():
    """
    Add a new Haram keyword
    
    Request body:
    {
        "keyword": "word",
        "language": "en"  // optional, default: "en"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        keyword = data.get('keyword')
        language = data.get('language', 'en')
        
        if not keyword:
            return jsonify({'error': 'keyword required'}), 400
        
        text_analyzer.add_keyword(keyword, language)
        
        return jsonify({
            'success': True,
            'message': f'Keyword added: {keyword} ({language})'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/keywords/remove', methods=['POST'])
def remove_keyword():
    """
    Remove a keyword
    
    Request body:
    {
        "keyword": "word",
        "language": "en"  // optional, default: "en"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        keyword = data.get('keyword')
        language = data.get('language', 'en')
        
        if not keyword:
            return jsonify({'error': 'keyword required'}), 400
        
        text_analyzer.remove_keyword(keyword, language)
        
        return jsonify({
            'success': True,
            'message': f'Keyword removed: {keyword} ({language})'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """404 handler"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 handler"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌙 Halal Browser AI Service")
    print("="*60)
    print(f"📍 Running on: http://127.0.0.1:5000")
    print(f"📖 API docs: http://127.0.0.1:5000")
    print(f"💚 Health check: http://127.0.0.1:5000/api/health")
    print("="*60 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        threaded=True
    )
