#!/usr/bin/env python3
"""
Configuration verification test script
"""
import sys
import os

try:
    import config
    print("✅ Config loaded successfully")
    print(f"Scene threshold: {config.SCENE_THRESHOLD}")
    print(f"Max scenes: {config.MAX_SCENES}")
    print(f"Whisper model: {config.WHISPER_MODEL}")
    print(f"GPT model: {config.GPT_MODEL}")
    
    if config.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        print("⚠️ OpenAI API Key not set - please update config.py")
    else:
        print("✅ OpenAI API Key is set")
        
    # Check required directories
    for directory in [config.VIDEOS_DIR, config.IMAGES_DIR, config.RESULTS_DIR]:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"📁 Directory will be created: {directory}")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")