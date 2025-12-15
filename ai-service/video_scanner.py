"""
Video Scanner - Frame-by-frame NSFW Detection
Analyzes video content by extracting and scanning frames
"""

import cv2
import os
import tempfile
from image_scanner import ImageScanner
import numpy as np


class VideoScanner:
    """
    Video content scanner using frame extraction and AI analysis
    """
    
    def __init__(self, image_scanner):
        """
        Initialize video scanner
        
        Args:
            image_scanner: ImageScanner instance for frame analysis
        """
        self.image_scanner = image_scanner
        print("✅ Video Scanner initialized")
    
    def extract_frames(self, video_path, fps=1, max_frames=30):
        """
        Extract frames from video at specified FPS
        
        Args:
            video_path: Path to video file
            fps: Frames per second to extract (default: 1 frame/second)
            max_frames: Maximum number of frames to extract
            
        Returns:
            List of frame numpy arrays
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / video_fps if video_fps > 0 else 0
        
        print(f"📹 Video info:")
        print(f"   FPS: {video_fps:.2f}")
        print(f"   Total frames: {total_frames}")
        print(f"   Duration: {duration:.2f}s")
        
        # Calculate frame interval
        frame_interval = int(video_fps / fps) if video_fps > 0 else 1
        
        frames = []
        frame_count = 0
        extracted_count = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Extract frame at interval
            if frame_count % frame_interval == 0:
                frames.append(frame)
                extracted_count += 1
                
                # Stop if max frames reached
                if extracted_count >= max_frames:
                    break
            
            frame_count += 1
        
        cap.release()
        
        print(f"✅ Extracted {len(frames)} frames")
        return frames
    
    def scan_frames(self, frames, threshold=0.7):
        """
        Scan extracted frames for NSFW content
        
        Args:
            frames: List of frame numpy arrays
            threshold: NSFW threshold
            
        Returns:
            List of scan results for each frame
        """
        results = []
        temp_dir = tempfile.mkdtemp()
        
        try:
            for i, frame in enumerate(frames):
                # Save frame temporarily
                temp_path = os.path.join(temp_dir, f"frame_{i:04d}.jpg")
                cv2.imwrite(temp_path, frame)
                
                # Scan frame
                result = self.image_scanner.scan(temp_path, threshold, use_cache=False)
                result['frame_number'] = i
                results.append(result)
                
                # Clean up temp file
                os.remove(temp_path)
                
                print(f"   Frame {i+1}/{len(frames)}: {result['decision']} (confidence: {result['confidence']:.2%})")
        
        finally:
            # Clean up temp directory
            try:
                os.rmdir(temp_dir)
            except:
                pass
        
        return results
    
    def scan(self, video_path, threshold=0.7, fps=1, max_frames=30, block_on_any=True):
        """
        Scan video for NSFW content
        
        Args:
            video_path: Path to video file
            threshold: NSFW threshold
            fps: Frames per second to extract
            max_frames: Maximum frames to analyze
            block_on_any: Block entire video if any frame is NSFW
            
        Returns:
            dict: {
                'is_safe': bool,
                'frames_analyzed': int,
                'unsafe_frames': int,
                'unsafe_frame_numbers': list,
                'max_confidence': float,
                'decision': str ('ALLOW', 'BLOCK'),
                'frame_results': list
            }
        """
        print(f"\n🔍 Scanning video: {video_path}")
        
        try:
            # Extract frames
            frames = self.extract_frames(video_path, fps, max_frames)
            
            if not frames:
                return {
                    'is_safe': True,
                    'frames_analyzed': 0,
                    'unsafe_frames': 0,
                    'unsafe_frame_numbers': [],
                    'max_confidence': 0.0,
                    'decision': 'ALLOW',
                    'error': 'No frames extracted'
                }
            
            # Scan frames
            frame_results = self.scan_frames(frames, threshold)
            
            # Analyze results
            unsafe_frames = [r for r in frame_results if r['is_nsfw']]
            unsafe_frame_numbers = [r['frame_number'] for r in unsafe_frames]
            max_confidence = max([r['confidence'] for r in frame_results]) if frame_results else 0.0
            
            # Determine decision
            if block_on_any:
                is_safe = len(unsafe_frames) == 0
                decision = 'ALLOW' if is_safe else 'BLOCK'
            else:
                # Block only if significant portion is unsafe
                unsafe_ratio = len(unsafe_frames) / len(frames)
                is_safe = unsafe_ratio < 0.3  # Less than 30% unsafe
                decision = 'ALLOW' if is_safe else 'BLOCK'
            
            result = {
                'is_safe': is_safe,
                'frames_analyzed': len(frames),
                'unsafe_frames': len(unsafe_frames),
                'unsafe_frame_numbers': unsafe_frame_numbers,
                'max_confidence': max_confidence,
                'decision': decision,
                'frame_results': frame_results
            }
            
            print(f"\n📊 Video scan result:")
            print(f"   Decision: {decision}")
            print(f"   Frames analyzed: {len(frames)}")
            print(f"   Unsafe frames: {len(unsafe_frames)}")
            print(f"   Max confidence: {max_confidence:.2%}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error scanning video: {e}")
            return {
                'is_safe': True,
                'frames_analyzed': 0,
                'unsafe_frames': 0,
                'unsafe_frame_numbers': [],
                'max_confidence': 0.0,
                'decision': 'ALLOW',
                'error': str(e)
            }
    
    def scan_url(self, video_url, threshold=0.7, fps=1, max_frames=30):
        """
        Scan video from URL
        
        Args:
            video_url: URL to video
            threshold: NSFW threshold
            fps: Frames per second to extract
            max_frames: Maximum frames to analyze
            
        Returns:
            Scan result dict
        """
        # Download video to temp file
        import requests
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_path = temp_file.name
        temp_file.close()
        
        try:
            print(f"📥 Downloading video from: {video_url}")
            response = requests.get(video_url, stream=True, timeout=30)
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Scan downloaded video
            result = self.scan(temp_path, threshold, fps, max_frames)
            
            return result
            
        finally:
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass


def main():
    """Test the video scanner"""
    print("🧪 Testing Video Scanner...")
    
    # Initialize image scanner
    model_path = "models/nsfw_model.onnx"
    
    if not os.path.exists(model_path):
        print(f"⚠️  Model not found: {model_path}")
        print("📥 Please download the model first")
        return
    
    from image_scanner import ImageScanner
    image_scanner = ImageScanner(model_path)
    
    # Initialize video scanner
    video_scanner = VideoScanner(image_scanner)
    
    # Test with sample video
    test_video = "tests/data/test_video.mp4"
    
    if os.path.exists(test_video):
        result = video_scanner.scan(test_video, threshold=0.7, fps=1, max_frames=10)
        print(f"\n✅ Test completed")
    else:
        print(f"⚠️  Test video not found: {test_video}")
        print("   Create a test video or provide a path to test")


if __name__ == "__main__":
    main()
