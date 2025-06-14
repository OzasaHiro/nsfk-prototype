#!/usr/bin/env python3
"""
NSFK? クイック分析ツール
YouTube URLを簡単に指定して分析するためのヘルパースクリプト
"""
import sys
from main import NSFKPrototype
import config

def quick_analyze(url_or_id):
    """指定されたYouTube URLの分析を実行"""
    print(f"🎯 Quick Analysis: {url_or_id}")
    print("="*50)
    
    # APIキー確認
    if config.DEMO_MODE:
        print("⚠️ Demo mode: Set OPENAI_API_KEY in .env for full analysis")
    
    # 分析実行
    nsfk = NSFKPrototype()
    result = nsfk.analyze_video(url_or_id)
    
    if result:
        safety = result['safety_analysis']
        video = result['video_info']
        
        print(f"\n🎬 {video['title']}")
        print(f"{safety['status_icon']} Score: {safety['final_score']}/100 ({safety['final_recommendation']})")
        print(f"📝 {safety['summary']}")
        
        if result.get('keywords'):
            print(f"🏷️ Keywords: {', '.join(result['keywords'][:5])}")
    else:
        print("❌ Analysis failed")

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_analyze.py <YouTube_URL_or_ID>")
        print("\nExamples:")
        print("  python quick_analyze.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("  python quick_analyze.py https://youtu.be/dQw4w9WgXcQ")
        print("  python quick_analyze.py dQw4w9WgXcQ")
        sys.exit(1)
    
    url_or_id = sys.argv[1]
    quick_analyze(url_or_id)

if __name__ == "__main__":
    main()