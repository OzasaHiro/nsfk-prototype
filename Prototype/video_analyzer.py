"""
Video Analysis Class
Integrates scene detection, visual analysis, and audio analysis
Based on scene.py, scene_analysis.py, transcription.py from Reference.md
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
        """Load Whisper model"""
        try:
            print(f"Loading Whisper model: {config.WHISPER_MODEL}")
            self.whisper_model = whisper.load_model(config.WHISPER_MODEL)
            print("✅ Whisper model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading Whisper model: {e}")
    
    def detect_scenes(self, video_path: str) -> List[Dict[str, Any]]:
        """
        Scene detection and representative frame extraction
        Based on scene.py from Reference.md
        """
        print(f"🎬 Starting scene detection: {video_path}")
        
        # Create image output folder
        if not os.path.exists(config.IMAGES_DIR):
            os.makedirs(config.IMAGES_DIR)
        
        try:
            # Open video and initialize SceneManager
            video = open_video(video_path)
            scene_manager = SceneManager()
            scene_manager.add_detector(ContentDetector(threshold=config.SCENE_THRESHOLD))

            # Analyze video to find scene boundaries
            scene_manager.detect_scenes(video)
            scene_list = scene_manager.get_scene_list()
            
            # Thin out scenes if exceeding the limit
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
                
                # Extract representative frame (scene start frame)
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
        Analyze image using GPT-4o-mini
        Prompt specialized for safety assessment
        """
        try:
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = self.openai_client.chat.completions.create(
                model=config.GPT_MODEL,
                max_tokens=config.MAX_TOKENS,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert in assessing the safety of children's content.
Analyze the image and objectively evaluate it from the following perspectives:
1. Violent content (weapons, fights, injuries, etc.)
2. Sexual content (inappropriate exposure, sexual expressions, etc.)
3. Inappropriate language (on-screen text, subtitles, etc.)
4. Drug and alcohol related content
5. Content that causes fear or anxiety

Please provide a concise and objective analysis in English."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please analyze the content of this image from the perspective of child safety. If there is text on the screen, please prioritize it in your consideration."
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
            return "Image analysis failed."
    
    def transcribe_audio(self, video_path: str) -> List[Dict[str, Any]]:
        """
        Audio transcription
        Based on transcription.py from Reference.md
        """
        if not self.whisper_model:
            print("❌ Whisper model not loaded")
            return []
        
        try:
            print("🎧 Starting audio transcription...")
            
            # Execute audio transcription
            result = self.whisper_model.transcribe(
                video_path, 
                verbose=config.VERBOSE, 
                fp16=False,
                language="ja"  # Japanese priority, auto-detection also possible
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
        Complete video analysis: Scene detection → Visual analysis → Audio analysis
        """
        print(f"🚀 Starting full video analysis: {video_path}")
        
        # Scene detection
        scenes = self.detect_scenes(video_path)
        
        # Visual analysis of each scene
        scene_analyses = []
        for scene in scenes:
            analysis = self.analyze_scene_image(scene['image_path'])
            scene_analyses.append({
                **scene,
                "visual_analysis": analysis
            })
        
        # Audio analysis
        audio_transcription = self.transcribe_audio(video_path)
        
        return {
            "scenes": scene_analyses,
            "audio": audio_transcription,
            "total_scenes": len(scene_analyses),
            "total_audio_segments": len(audio_transcription)
        }

if __name__ == "__main__":
    # For testing
    analyzer = VideoAnalyzer()
    
    # Configuration check
    print(f"Config check:")
    print(f"- Whisper model: {config.WHISPER_MODEL}")
    print(f"- GPT model: {config.GPT_MODEL}")
    print(f"- Scene threshold: {config.SCENE_THRESHOLD}")
    print(f"- Max scenes: {config.MAX_SCENES}")
    
    # Execute analysis if test video exists
    test_video = "./videos/test.mp4"
    if os.path.exists(test_video):
        result = analyzer.analyze_full_video(test_video)
        print(f"Analysis completed: {result['total_scenes']} scenes, {result['total_audio_segments']} audio segments")