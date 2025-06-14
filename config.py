"""
NSFK? プロトタイプ設定ファイル
"""
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# OpenAI API設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# デモ用設定（APIキーが設定されていない場合のテスト用）
DEMO_MODE = not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE"

# 動画分析設定
SCENE_THRESHOLD = 60.0  # シーン検出感度（高い値＝鈍感）
MAX_SCENES = 20  # プロトタイプでは最大20シーンに制限
WHISPER_MODEL = "base"  # 速度重視（base, small, medium, large）
GPT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 5000  # コスト節約のため制限

# ファイルパス設定
VIDEOS_DIR = "./videos"
IMAGES_DIR = "./images"
RESULTS_DIR = "./results"

# 安全性スコアリング設定
SAFETY_CATEGORIES = {
    "violence": {"weight": 0.3, "threshold": 15},
    "sexual_content": {"weight": 0.4, "threshold": 10},
    "language": {"weight": 0.2, "threshold": 20},
    "drugs": {"weight": 0.1, "threshold": 15}
}

# 安全性判定基準
SCORE_THRESHOLDS = {
    "safe": 80,      # 80点以上：推奨
    "caution": 60,   # 60-79点：注意
    "unsafe": 0      # 59点以下：非推奨
}

# デバッグ設定
DEBUG = True
VERBOSE = True

# よく使われるテスト動画ID
TEST_VIDEOS = {
    "rick_roll": "dQw4w9WgXcQ",           # Rick Astley - Never Gonna Give You Up
    "baby_shark": "XqZsoesa55w",          # Baby Shark Dance (子供向け)
    "cocomelon": "D9tAKLTktY0",          # CoComelon Nursery Rhymes
    "educational": "rN6nlNC9WQA",        # 教育系動画例
    "minecraft": "I-sH53vXP2A",         # Minecraft動画例
}