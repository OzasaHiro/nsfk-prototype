"""
NSFK? Prototype Configuration File
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Demo configuration (for testing when API key is not set)
DEMO_MODE = not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE"

# Video Analysis Configuration
SCENE_THRESHOLD = 60.0  # Scene detection sensitivity (higher value = less sensitive)
MAX_SCENES = 20  # Limited to maximum 20 scenes for prototype
WHISPER_MODEL = "base"  # Speed-focused (base, small, medium, large)
GPT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 5000  # Limited for cost savings

# File Path Configuration
VIDEOS_DIR = "./videos"
IMAGES_DIR = "./images"
RESULTS_DIR = "./results"

# Safety Scoring Configuration
SAFETY_CATEGORIES = {
    "violence": {"weight": 0.3, "threshold": 15},
    "sexual_content": {"weight": 0.4, "threshold": 10},
    "language": {"weight": 0.2, "threshold": 20},
    "drugs": {"weight": 0.1, "threshold": 15}
}

# Safety Assessment Criteria
SCORE_THRESHOLDS = {
    "safe": 80,      # 80+ points: Recommended
    "caution": 60,   # 60-79 points: Caution
    "unsafe": 0      # 59 points or below: Not recommended
}

# Debug Configuration
DEBUG = True
VERBOSE = True

# Frequently Used Test Video IDs
TEST_VIDEOS = {
    "rick_roll": "dQw4w9WgXcQ",           # Rick Astley - Never Gonna Give You Up
    "baby_shark": "XqZsoesa55w",          # Baby Shark Dance (for children)
    "cocomelon": "D9tAKLTktY0",          # CoComelon Nursery Rhymes
    "educational": "rN6nlNC9WQA",        # Educational video example
    "minecraft": "I-sH53vXP2A",         # Minecraft video example
}