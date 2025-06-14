#!/usr/bin/env python3
"""
NSFK? Quick Analysis Tool
Helper script for easily analyzing specified YouTube URLs
"""
import sys
from main import NSFKPrototype
import config

def quick_analyze(url_or_id):
    """Execute analysis of the specified YouTube URL"""
    print(f"🎯 Quick Analysis: {url_or_id}")
    print("="*50)
    
    # Check API key
    if config.DEMO_MODE:
        print("⚠️ Demo mode: Set OPENAI_API_KEY in .env for full analysis")
    
    # Execute analysis
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