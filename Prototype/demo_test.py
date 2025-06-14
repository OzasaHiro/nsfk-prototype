#!/usr/bin/env python3
"""
NSFK? Prototype Demo Test (can verify operation without API key)
"""
import os
import time
from youtube_downloader import YouTubeDownloader
import config

def test_youtube_downloader():
    """Test YouTube Downloader"""
    print("🎬 Testing YouTube Downloader...")
    
    downloader = YouTubeDownloader()
    
    # Short test video (Rick Astley - Never Gonna Give You Up)
    test_video_id = "dQw4w9WgXcQ"
    
    print(f"Downloading test video: {test_video_id}")
    success, file_path, info = downloader.download_video(test_video_id)
    
    if success:
        print(f"✅ Download successful!")
        print(f"   File: {file_path}")
        print(f"   Title: {info['title']}")
        print(f"   Duration: {info['duration']}s")
        return file_path
    else:
        print(f"❌ Download failed: {info.get('error', 'Unknown error')}")
        return None

def test_scene_detection(video_path):
    """Test scene detection (no API key required)"""
    if not video_path or not os.path.exists(video_path):
        print("⚠️ Video file not found, skipping scene detection test")
        return
    
    print("🎯 Testing Scene Detection...")
    
    try:
        from video_analyzer import VideoAnalyzer
        analyzer = VideoAnalyzer()
        
        # Scene detection only (skip GPT analysis)
        scenes = analyzer.detect_scenes(video_path)
        
        if scenes:
            print(f"✅ Scene detection successful!")
            print(f"   Detected {len(scenes)} scenes")
            for i, scene in enumerate(scenes[:3]):  # Display only first 3 scenes
                print(f"   Scene {i+1}: {scene['start_time']:.2f}s - {scene['end_time']:.2f}s")
        else:
            print("❌ Scene detection failed")
            
    except Exception as e:
        print(f"❌ Scene detection error: {e}")

def test_whisper_basic():
    """Basic Whisper test (with small file)"""
    print("🎧 Testing Whisper (basic)...")
    
    try:
        import whisper
        
        # Model loading test
        print(f"Loading Whisper model: {config.WHISPER_MODEL}")
        model = whisper.load_model(config.WHISPER_MODEL)
        print("✅ Whisper model loaded successfully")
        
        # Test if actual audio file exists
        test_video = "./videos/dQw4w9WgXcQ.mp4"
        if os.path.exists(test_video):
            print("Testing audio transcription...")
            result = model.transcribe(test_video, fp16=False)
            if result.get('text'):
                print(f"✅ Transcription successful: {result['text'][:100]}...")
            else:
                print("⚠️ No transcription result")
        else:
            print("ℹ️ No test video found, skipping transcription test")
            
    except Exception as e:
        print(f"❌ Whisper test error: {e}")

def main():
    """Main execution of demo test"""
    print("🛡️ NSFK? Prototype Demo Test")
    print("=" * 50)
    print(f"Demo mode: {config.DEMO_MODE}")
    print()
    
    start_time = time.time()
    
    # 1. YouTube Downloader test
    video_path = test_youtube_downloader()
    print()
    
    # 2. Scene Detection test
    test_scene_detection(video_path)
    print()
    
    # 3. Basic Whisper test
    test_whisper_basic()
    print()
    
    elapsed_time = time.time() - start_time
    print("=" * 50)
    print(f"✅ Demo test completed in {elapsed_time:.2f}s")
    print()
    
    if config.DEMO_MODE:
        print("📝 To run full analysis:")
        print("1. Set your OpenAI API key in config.py")
        print("2. Run: python main.py")
    else:
        print("🚀 Ready for full analysis! Run: python main.py")

if __name__ == "__main__":
    main()