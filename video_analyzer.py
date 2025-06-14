"""
動画分析クラス
シーン検出、映像分析、音声分析を統合
Reference.mdのscene.py、scene_analysis.py、transcription.pyをベースに統合
"""
import cv2
import os
import base64
import whisper
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from openai import OpenAI
from typing import List, Dict, Any
import config

class VideoAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.whisper_model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Whisperモデルの読み込み"""
        try:
            print(f"Loading Whisper model: {config.WHISPER_MODEL}")
            self.whisper_model = whisper.load_model(config.WHISPER_MODEL)
            print("✅ Whisper model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading Whisper model: {e}")
    
    def detect_scenes(self, video_path: str) -> List[Dict[str, Any]]:
        """
        シーン検出と代表フレーム抽出
        Reference.mdのscene.pyをベース
        """
        print(f"🎬 Starting scene detection: {video_path}")
        
        # 画像出力フォルダ作成
        if not os.path.exists(config.IMAGES_DIR):
            os.makedirs(config.IMAGES_DIR)
        
        try:
            # Videoを開き、SceneManagerの初期化
            video = open_video(video_path)
            scene_manager = SceneManager()
            scene_manager.add_detector(ContentDetector(threshold=config.SCENE_THRESHOLD))

            # 動画を解析してシーンの境界を見つける
            scene_manager.detect_scenes(video)
            scene_list = scene_manager.get_scene_list()
            
            # 制限数を超える場合は間引き
            if len(scene_list) > config.MAX_SCENES:
                step = len(scene_list) // config.MAX_SCENES
                scene_list = scene_list[::step][:config.MAX_SCENES]
                print(f"⚠️ Too many scenes detected. Limited to {config.MAX_SCENES}")
            
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            scenes_data = []
            
            for i, scene in enumerate(scene_list):
                start_frame = scene[0].get_frames()
                end_frame = scene[1].get_frames() - 1
                start_time = start_frame / fps
                end_time = end_frame / fps
                
                # 代表フレーム抽出（シーン開始フレーム）
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                ret, frame = cap.read()
                
                if ret:
                    image_path = f"{config.IMAGES_DIR}/scene_{i + 1}_frame_{start_frame}.jpg"
                    cv2.imwrite(image_path, frame)
                    
                    scenes_data.append({
                        "scene_number": i + 1,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration": end_time - start_time,
                        "image_path": image_path
                    })
            
            cap.release()
            print(f"✅ Scene detection completed: {len(scenes_data)} scenes")
            return scenes_data
            
        except Exception as e:
            print(f"❌ Scene detection error: {e}")
            return []
    
    def analyze_scene_image(self, image_path: str) -> str:
        """
        画像をGPT-4o-miniで分析
        安全性判定に特化したプロンプト
        """
        try:
            # 画像をbase64エンコード
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = self.openai_client.chat.completions.create(
                model=config.GPT_MODEL,
                max_tokens=config.MAX_TOKENS,
                messages=[
                    {
                        "role": "system",
                        "content": """あなたは子供向けコンテンツの安全性を判定する専門家です。
画像を分析し、以下の観点で客観的に評価してください：
1. 暴力的な内容（武器、喖嘩、怠我など）
2. 性的な内容（不適切な露出、性的な表現など）
3. 不適切な言語（画面上のテキスト、字幕など）
4. 薬物・アルコール関連
5. 恐怖・不安を与える内容

簡潔で客観的な分析を日本語で回答してください。"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "この画像の内容を子供の安全性の観点から分析してください。画面上のテキストがある場合は優先的に考慮してください。"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "low"
                                }
                            }
                        ]
                    }
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Image analysis error: {e}")
            return "画像分析に失敗しました。"
    
    def transcribe_audio(self, video_path: str) -> List[Dict[str, Any]]:
        """
        音声の文字起こし
        Reference.mdのtranscription.pyをベース
        """
        if not self.whisper_model:
            print("❌ Whisper model not loaded")
            return []
        
        try:
            print("🎧 Starting audio transcription...")
            
            # 音声文字起こし実行
            result = self.whisper_model.transcribe(
                video_path, 
                verbose=config.VERBOSE, 
                fp16=False,
                language="ja"  # 日本語優先、自動検出も可能
            )
            
            segments = result['segments']
            transcription_data = [
                {
                    "start": segment['start'],
                    "end": segment['end'],
                    "text": segment['text'].strip(),
                    "confidence": segment.get('no_speech_prob', 0.0)
                } for segment in segments if segment['text'].strip()
            ]
            
            print(f"✅ Audio transcription completed: {len(transcription_data)} segments")
            return transcription_data
            
        except Exception as e:
            print(f"❌ Audio transcription error: {e}")
            return []
    
    def analyze_full_video(self, video_path: str) -> Dict[str, Any]:
        """
        動画の完全分析：シーン検出→映像分析→音声分析
        """
        print(f"🚀 Starting full video analysis: {video_path}")
        
        # シーン検出
        scenes = self.detect_scenes(video_path)
        
        # 各シーンの映像分析
        scene_analyses = []
        for scene in scenes:
            analysis = self.analyze_scene_image(scene['image_path'])
            scene_analyses.append({
                **scene,
                "visual_analysis": analysis
            })
        
        # 音声分析
        audio_transcription = self.transcribe_audio(video_path)
        
        return {
            "scenes": scene_analyses,
            "audio": audio_transcription,
            "total_scenes": len(scene_analyses),
            "total_audio_segments": len(audio_transcription)
        }

if __name__ == "__main__":
    # テスト用
    analyzer = VideoAnalyzer()
    
    # 設定確認
    print(f"Config check:")
    print(f"- Whisper model: {config.WHISPER_MODEL}")
    print(f"- GPT model: {config.GPT_MODEL}")
    print(f"- Scene threshold: {config.SCENE_THRESHOLD}")
    print(f"- Max scenes: {config.MAX_SCENES}")
    
    # テスト動画があれば分析実行
    test_video = "./videos/test.mp4"
    if os.path.exists(test_video):
        result = analyzer.analyze_full_video(test_video)
        print(f"Analysis completed: {result['total_scenes']} scenes, {result['total_audio_segments']} audio segments")