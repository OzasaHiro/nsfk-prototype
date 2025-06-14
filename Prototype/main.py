"""
NSFK? Prototype Main File
Executes YouTube video safety analysis
"""
import os
import time
import json
import shutil
from datetime import datetime
from typing import Optional

from youtube_downloader import YouTubeDownloader
from video_analyzer import VideoAnalyzer
from safety_scorer import SafetyScorer
import config

class NSFKPrototype:
    def __init__(self):
        self.downloader = YouTubeDownloader(config.VIDEOS_DIR)
        self.analyzer = VideoAnalyzer()
        self.scorer = SafetyScorer()
        
        # Create necessary directories
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary directories"""
        for directory in [config.VIDEOS_DIR, config.IMAGES_DIR, config.RESULTS_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"📁 Created directory: {directory}")
    
    def _cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(config.VIDEOS_DIR):
                shutil.rmtree(config.VIDEOS_DIR)
                os.makedirs(config.VIDEOS_DIR)
            
            if os.path.exists(config.IMAGES_DIR):
                shutil.rmtree(config.IMAGES_DIR)
                os.makedirs(config.IMAGES_DIR)
            
            print("🧹 Temporary files cleaned up")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def analyze_video(self, youtube_url: str, cleanup: bool = True) -> Optional[dict]:
        """
        Execute complete analysis of YouTube video
        
        Args:
            youtube_url: YouTube URL or video ID
            cleanup: Whether to delete temporary files after analysis
            
        Returns:
            dict: Analysis results, None if failed
        """
        start_time = time.time()
        print(f"🚀 Starting NSFK? analysis for: {youtube_url}")
        print("="*60)
        
        try:
            # 1. Video download
            print("📥 Step 1: Downloading video...")
            success, video_path, video_info = self.downloader.download_video(youtube_url)
            
            if not success:
                print(f"❌ Download failed: {video_info.get('error', 'Unknown error')}")
                return None
            
            print(f"✅ Downloaded: {video_info['title']}")
            print(f"   Duration: {video_info['duration']}s")
            print()
            
            # 2. Video analysis
            print("🎬 Step 2: Analyzing video content...")
            analysis_result = self.analyzer.analyze_full_video(video_path)
            
            if not analysis_result['scenes']:
                print("❌ Video analysis failed: No scenes detected")
                return None
                
            print(f"✅ Video analysis completed")
            print(f"   Scenes detected: {analysis_result['total_scenes']}")
            print(f"   Audio segments: {analysis_result['total_audio_segments']}")
            print()
            
            # 3. Safety analysis
            print("🛡️ Step 3: Safety analysis...")
            safety_analysis = self.scorer.analyze_content_with_gpt(
                analysis_result['scenes'], 
                analysis_result['audio']
            )
            
            # 4. Generate final report
            print("📊 Step 4: Generating final report...")
            final_report = self.scorer.generate_safety_report(video_info, safety_analysis)
            final_report['processing_timestamp'] = datetime.now().isoformat()
            final_report['processing_time'] = round(time.time() - start_time, 2)
            final_report['video_url'] = youtube_url
            
            # 5. Save results
            self._save_results(final_report, youtube_url)
            
            # 6. Display results
            self._display_results(final_report)
            
            # 7. Cleanup
            if cleanup:
                self._cleanup_temp_files()
            
            print("="*60)
            print(f"✅ Analysis completed in {final_report['processing_time']}s")
            
            return final_report
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            if config.DEBUG:
                import traceback
                traceback.print_exc()
            return None
    
    def _save_results(self, report: dict, youtube_url: str):
        """結果をファイルに保存"""
        try:
            # ファイル名生成（安全な文字のみ）
            video_id = self.downloader.extract_video_id(youtube_url)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nsfk_analysis_{video_id}_{timestamp}.json"
            filepath = os.path.join(config.RESULTS_DIR, filename)
            
            # JSON保存
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Results saved: {filepath}")
            
            # 人間が読みやすいテキスト版も保存
            txt_filename = filename.replace('.json', '.txt')
            txt_filepath = os.path.join(config.RESULTS_DIR, txt_filename)
            
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                self._write_human_readable_report(f, report)
                
            print(f"📄 Human-readable report: {txt_filepath}")
            
        except Exception as e:
            print(f"⚠️ Save error: {e}")
    
    def _write_human_readable_report(self, file, report: dict):
        """Output report in human-readable format"""
        safety = report['safety_analysis']
        video = report['video_info']
        
        file.write("NSFK? - YouTube Video Safety Analysis Report\\n")
        file.write("="*50 + "\\n\\n")
        
        file.write(f"Video Title: {video['title']}\\n")
        file.write(f"Uploader: {video['uploader']}\\n")
        file.write(f"Duration: {video['duration']} seconds\\n")
        file.write(f"Analysis Date: {report['processing_timestamp']}\\n")
        file.write(f"Processing Time: {report['processing_time']} seconds\\n\\n")
        
        file.write("【Safety Assessment】\\n")
        file.write(f"{safety['status_icon']} Overall Score: {safety['final_score']}/100\\n")
        file.write(f"Recommendation Level: {safety['final_recommendation']}\\n\\n")
        
        file.write("【Summary】\\n")
        file.write(f"{safety['summary']}\\n\\n")
        
        if safety.get('key_concerns'):
            file.write("【Key Concerns】\\n")
            for concern in safety['key_concerns']:
                file.write(f"• {concern}\\n")
            file.write("\\n")
        
        if safety.get('positive_aspects'):
            file.write("【Positive Aspects】\\n")
            for aspect in safety['positive_aspects']:
                file.write(f"• {aspect}\\n")
            file.write("\\n")
        
        if report.get('keywords'):
            file.write("【Keywords】\\n")
            file.write(", ".join(report['keywords']) + "\\n\\n")
        
        file.write("【Detailed Scores】\\n")
        risk_categories = safety.get('risk_categories', {})
        for category, score in risk_categories.items():
            file.write(f"{category}: {score}/25\\n")
    
    def _display_results(self, report: dict):
        """Display results to console"""
        safety = report['safety_analysis']
        video = report['video_info']
        
        print("\\n" + "="*60)
        print("📋 ANALYSIS RESULTS")
        print("="*60)
        print(f"🎬 Video: {video['title']}")
        print(f"⏱️ Duration: {video['duration']}s | Processing: {report['processing_time']}s")
        print()
        print(f"{safety['status_icon']} Safety Score: {safety['final_score']}/100")
        print(f"🎯 Recommendation: {safety['final_recommendation']}")
        print()
        print(f"📝 Summary: {safety['summary']}")
        
        if safety.get('key_concerns'):
            print("\\n⚠️ Key Concerns:")
            for concern in safety['key_concerns']:
                print(f"   • {concern}")
        
        if safety.get('positive_aspects'):
            print("\\n✅ Positive Aspects:")
            for aspect in safety['positive_aspects']:
                print(f"   • {aspect}")
        
        if report.get('keywords'):
            print(f"\\n🏷️ Keywords: {', '.join(report['keywords'])}")

def main():
    """Main execution function"""
    print("🛡️ NSFK? (Not Safe For Kids?) - Prototype")
    print("YouTube Video Safety Analyzer for Parents")
    print("="*60)
    
    # Configuration check
    if config.DEMO_MODE:
        print("⚠️ Demo mode: OpenAI API key not set")
        print("   Limited functionality - GPT analysis will be skipped")
        print("   Set your API key in .env file for full analysis")
        print()
    
    # Initialize prototype
    nsfk = NSFKPrototype()
    
    # Get YouTube URL
    youtube_url = None
    
    # 1. From command line arguments
    if len(os.sys.argv) > 1:
        youtube_url = os.sys.argv[1]
        print(f"🎬 Using URL from command line: {youtube_url}")
    
    # 2. From user input
    else:
        print("📝 Please specify a YouTube video:")
        print("   • Full URL: https://www.youtube.com/watch?v=VIDEO_ID")
        print("   • Short URL: https://youtu.be/VIDEO_ID") 
        print("   • Video ID only: VIDEO_ID")
        print("   • Leave blank to use demo video")
        print()
        
        youtube_url = input("YouTube URL or Video ID: ").strip()
        
        if not youtube_url:
            # Demo short video ID
            youtube_url = "dQw4w9WgXcQ"  # Rick Astley (for testing)
            print(f"📺 Using demo video: {youtube_url}")
        
        # URL validation and user-friendly display
        downloader = YouTubeDownloader()
        video_id = downloader.extract_video_id(youtube_url)
        if video_id:
            print(f"✅ Video ID detected: {video_id}")
            print(f"🔗 Full URL: https://www.youtube.com/watch?v={video_id}")
        else:
            print(f"⚠️ Invalid URL format. Trying anyway: {youtube_url}")
    
    print()
    
    # Execute analysis
    result = nsfk.analyze_video(youtube_url)
    
    if result:
        print("\\n✅ Analysis completed successfully!")
        print(f"📁 Results saved to: {config.RESULTS_DIR}")
        
        # Display result files
        import glob
        recent_files = sorted(glob.glob(f"{config.RESULTS_DIR}/*.json"))
        if recent_files:
            latest_file = recent_files[-1]
            print(f"📄 Latest result: {latest_file}")
            
    else:
        print("\\n❌ Analysis failed. Please check the video URL and try again.")
        print("\\n💡 Troubleshooting:")
        print("   • Verify the YouTube URL is correct and public")
        print("   • Check your internet connection")
        print("   • Try using just the video ID (11 characters)")
        print("   • Run demo_test.py for basic functionality test")

if __name__ == "__main__":
    main()