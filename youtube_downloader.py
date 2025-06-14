"""
YouTube動画ダウンロード機能
Reference.mdのyoutube_dl.pyをベースに、プロトタイプ向けに改良
"""
import yt_dlp
import os
from typing import Optional

class YouTubeDownloader:
    def __init__(self, output_path: str = "./videos"):
        self.output_path = output_path
        self._ensure_directory()
    
    def _ensure_directory(self):
        """出力ディレクトリが存在しない場合は作成"""
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """YouTube URLから動画IDを抽出"""
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        else:
            # URLがすでに動画IDの場合
            return url if len(url) == 11 else None
    
    def download_video(self, url_or_id: str) -> tuple[bool, str, dict]:
        """
        YouTube動画をダウンロード
        
        Args:
            url_or_id: YouTube URL または 動画ID
            
        Returns:
            tuple: (成功フラグ, ファイルパス, 動画情報)
        """
        video_id = self.extract_video_id(url_or_id)
        if not video_id:
            return False, "", {"error": "Invalid YouTube URL or ID"}
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        try:
            # yt-dlpオプション設定
            ydl_opts = {
                'format': 'best[height<=720]/best',  # 720p以下で最高品質
                'outtmpl': f'{self.output_path}/{video_id}.%(ext)s',
                'noplaylist': True,  # プレイリストは無視
                'extract_flat': False,
            }

            # ダウンロード実行
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 動画情報取得
                info = ydl.extract_info(video_url, download=False)
                video_info = {
                    "title": info.get("title", "Unknown"),
                    "duration": info.get("duration", 0),
                    "description": info.get("description", ""),
                    "uploader": info.get("uploader", "Unknown"),
                    "view_count": info.get("view_count", 0),
                    "upload_date": info.get("upload_date", ""),
                }
                
                # ダウンロード実行
                ydl.download([video_url])
                
                # ダウンロードされたファイルのパスを特定
                for ext in ['mp4', 'webm', 'mkv']:
                    file_path = f'{self.output_path}/{video_id}.{ext}'
                    if os.path.exists(file_path):
                        print(f"Download completed: {file_path}")
                        return True, file_path, video_info
                
                return False, "", {"error": "Downloaded file not found"}
                
        except Exception as e:
            print(f"Download error: {e}")
            return False, "", {"error": str(e)}

if __name__ == "__main__":
    # テスト用
    downloader = YouTubeDownloader()
    
    # テスト動画ID（短い動画）
    test_video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    success, file_path, info = downloader.download_video(test_video_id)
    if success:
        print(f"✅ Download successful: {file_path}")
        print(f"📝 Title: {info['title']}")
        print(f"⏱️ Duration: {info['duration']}s")
    else:
        print(f"❌ Download failed: {info.get('error', 'Unknown error')}")