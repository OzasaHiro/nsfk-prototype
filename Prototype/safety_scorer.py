"""
Safety Scoring Module
Calculates child-friendly safety scores from video and audio analysis results
"""
import re
from typing import Dict, List, Any
from openai import OpenAI
import config
import json

class SafetyScorer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        # Risk keywords dictionary
        self.risk_keywords = {
            "violence": ["violence", "weapon", "blood", "injury", "fight", "hit", "kick", "war", "death"],
            "sexual_content": ["sexual", "naked", "underwear", "adult", "romance", "kiss"],
            "language": ["stupid", "die", "kill", "annoying", "gross", "ugly", "fat"],
            "drugs": ["alcohol", "cigarette", "tobacco", "beer", "liquor", "drinking", "smoking"]
        }
    
    def analyze_text_safety(self, text: str) -> Dict[str, Any]:
        """
        Text safety analysis
        Keyword-based + GPT analysis
        """
        text_lower = text.lower()
        
        # Keyword matching
        category_scores = {}
        detected_keywords = {}
        
        for category, keywords in self.risk_keywords.items():
            found_keywords = [kw for kw in keywords if kw in text]
            detected_keywords[category] = found_keywords
            
            # Score calculation (based on keyword count)
            risk_score = min(len(found_keywords) * 10, 50)  # Maximum 50 point deduction
            category_scores[category] = risk_score
        
        return {
            "category_scores": category_scores,
            "detected_keywords": detected_keywords,
            "total_risk_score": sum(category_scores.values())
        }
    
    def analyze_content_with_gpt(self, scenes: List[Dict], audio: List[Dict]) -> Dict[str, Any]:
        """
        Comprehensive safety analysis using GPT
        """
        try:
            # Combine scene analysis
            scene_summaries = []
            for scene in scenes[:10]:  # Only first 10 scenes (token saving)
                scene_summaries.append(f"Scene {scene['scene_number']}: {scene['visual_analysis']}")
            
            # Combine audio text
            audio_text = " ".join([seg['text'] for seg in audio[:20]])  # First 20 segments
            
            prompt = f"""
Please analyze the following video content from a child safety perspective (ages 5-12).

【Visual Analysis】:
{chr(10).join(scene_summaries)}

【Audio Content】:
{audio_text}

Please respond in the following JSON format:
{{
    "overall_safety_score": safety score from 0-100,
    "risk_categories": {{
        "violence": risk score from 0-25,
        "sexual_content": risk score from 0-25,
        "language": risk score from 0-25,
        "drugs": risk score from 0-25
    }},
    "summary": "concise 1-2 line summary",
    "key_concerns": ["concern 1", "concern 2"],
    "positive_aspects": ["positive aspect 1", "positive aspect 2"],
    "recommendation": "recommended/caution/not recommended"
}}

Please evaluate with high score = safe, low score = dangerous.
"""

            response = self.openai_client.chat.completions.create(
                model=config.GPT_MODEL,
                max_tokens=config.MAX_TOKENS,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in child content safety evaluation. Please provide objective and constructive assessments."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse GPT response as JSON
            gpt_response = response.choices[0].message.content
            
            # Extract JSON portion
            json_start = gpt_response.find('{')
            json_end = gpt_response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = gpt_response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback when JSON is not found
                return self._create_fallback_analysis(gpt_response)
                
        except Exception as e:
            print(f"❌ GPT analysis error: {e}")
            return self._create_fallback_analysis("GPT analysis failed")
    
    def _create_fallback_analysis(self, error_msg: str = "") -> Dict[str, Any]:
        """
        Fallback for GPT analysis failure
        """
        return {
            "overall_safety_score": 50,
            "risk_categories": {
                "violence": 10,
                "sexual_content": 10,
                "language": 10,
                "drugs": 10
            },
            "summary": f"Automatic analysis failed. Manual verification required. {error_msg}",
            "key_concerns": ["Analysis error"],
            "positive_aspects": ["Not evaluated"],
            "recommendation": "caution"
        }
    
    def calculate_final_score(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate final safety score and recommendation
        """
        score = analysis_result.get("overall_safety_score", 50)
        
        # Recommendation level based on score
        if score >= config.SCORE_THRESHOLDS["safe"]:
            recommendation = "recommended"
            status = "safe"
            icon = "✅"
        elif score >= config.SCORE_THRESHOLDS["caution"]:
            recommendation = "caution"
            status = "caution"
            icon = "⚠️"
        else:
            recommendation = "not recommended"
            status = "unsafe"
            icon = "❌"
        
        return {
            **analysis_result,
            "final_score": score,
            "final_recommendation": recommendation,
            "status": status,
            "status_icon": icon
        }
    
    def generate_safety_report(self, video_info: Dict, analysis_result: Dict) -> Dict[str, Any]:
        """
        Generate final safety report
        """
        safety_analysis = self.calculate_final_score(analysis_result)
        
        # Keyword extraction
        summary_text = safety_analysis.get("summary", "")
        keywords = []
        
        # Basic keyword extraction (can be improved)
        common_words = ["education", "learning", "fun", "interesting", "experiment", "craft", "music", "song", "dance"]
        for word in common_words:
            if word in summary_text or any(word in seg.get('text', '') for seg in analysis_result.get('audio_segments', [])):
                keywords.append(word)
        
        return {
            "video_info": {
                "title": video_info.get("title", "Unknown"),
                "duration": video_info.get("duration", 0),
                "uploader": video_info.get("uploader", "Unknown")
            },
            "safety_analysis": safety_analysis,
            "keywords": keywords[:10],  # Maximum 10
            "processing_timestamp": None,  # Set later
            "version": "prototype-v1.0"
        }

if __name__ == "__main__":
    # For testing
    scorer = SafetyScorer()
    
    # Test dummy data
    test_scenes = [
        {"scene_number": 1, "visual_analysis": "Children studying in a bright classroom"},
        {"scene_number": 2, "visual_analysis": "Teacher teaching math on the blackboard"}
    ]
    
    test_audio = [
        {"text": "Let's study arithmetic today"},
        {"text": "Let's all calculate together"}
    ]
    
    analysis = scorer.analyze_content_with_gpt(test_scenes, test_audio)
    final_report = scorer.generate_safety_report({"title": "Test Video", "duration": 300}, analysis)
    
    print("Safety Analysis Test:")
    print(f"Score: {final_report['safety_analysis']['final_score']}")
    print(f"Recommendation: {final_report['safety_analysis']['final_recommendation']}")
    print(f"Summary: {final_report['safety_analysis']['summary']}")