"""
安全性スコアリング機能
動画・音声分析結果から子供向け安全性スコアを算出
"""
import re
from typing import Dict, List, Any
from openai import OpenAI
import config
import json

class SafetyScorer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        # 危険キーワード辞書
        self.risk_keywords = {
            "violence": ["暴力", "武器", "血", "怠我", "喖嘩", "殴る", "蹴る", "戦争", "死"],
            "sexual_content": ["性的", "裸", "下着", "大人", "恋愛", "キス"],
            "language": ["馬鹿", "死ね", "殺す", "うざい", "きもい", "ブス", "デブ"],
            "drugs": ["酒", "タバコ", "煙草", "ビール", "お酒", "飲酒", "吸煙"]
        }
    
    def analyze_text_safety(self, text: str) -> Dict[str, Any]:
        """
        テキストの安全性分析
        キーワードベース + GPT分析
        """
        text_lower = text.lower()
        
        # キーワードマッチング
        category_scores = {}
        detected_keywords = {}
        
        for category, keywords in self.risk_keywords.items():
            found_keywords = [kw for kw in keywords if kw in text]
            detected_keywords[category] = found_keywords
            
            # スコア計算（キーワード数に基づく）
            risk_score = min(len(found_keywords) * 10, 50)  # 最大50点減点
            category_scores[category] = risk_score
        
        return {
            "category_scores": category_scores,
            "detected_keywords": detected_keywords,
            "total_risk_score": sum(category_scores.values())
        }
    
    def analyze_content_with_gpt(self, scenes: List[Dict], audio: List[Dict]) -> Dict[str, Any]:
        """
        GPTを使用した総合的な安全性分析
        """
        try:
            # シーン分析の結合
            scene_summaries = []
            for scene in scenes[:10]:  # 最初の10シーンのみ（トークン節約）
                scene_summaries.append(f"シーン{scene['scene_number']}: {scene['visual_analysis']}")
            
            # 音声テキストの結合
            audio_text = " ".join([seg['text'] for seg in audio[:20]])  # 最初の20セグメント
            
            prompt = f"""
以下の動画コンテンツを子供（5-12歳）の安全性の観点から分析してください。

【映像分析】:
{chr(10).join(scene_summaries)}

【音声内容】:
{audio_text}

以下の形式でJSON回答してください：
{{
    "overall_safety_score": 0-100の安全性スコア,
    "risk_categories": {{
        "violence": 0-25のリスクスコア,
        "sexual_content": 0-25のリスクスコア,
        "language": 0-25のリスクスコア,
        "drugs": 0-25のリスクスコア
    }},
    "summary": "1-2行の簡潔なサマリー",
    "key_concerns": ["懸念点1", "懸念点2"],
    "positive_aspects": ["良い点1", "良い点2"],
    "recommendation": "推奨/注意/非推奨"
}}

高いスコア＝安全、低いスコア＝危険として評価してください。
"""

            response = self.openai_client.chat.completions.create(
                model=config.GPT_MODEL,
                max_tokens=config.MAX_TOKENS,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは子供向けコンテンツの安全性評価の専門家です。客観的で建設的な評価を行ってください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # GPTの回答をJSON解析
            gpt_response = response.choices[0].message.content
            
            # JSON部分を抽出
            json_start = gpt_response.find('{')
            json_end = gpt_response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = gpt_response[json_start:json_end]
                return json.loads(json_str)
            else:
                # JSONが見つからない場合のフォールバック
                return self._create_fallback_analysis(gpt_response)
                
        except Exception as e:
            print(f"❌ GPT analysis error: {e}")
            return self._create_fallback_analysis("GPT分析に失敗しました")
    
    def _create_fallback_analysis(self, error_msg: str = "") -> Dict[str, Any]:
        """
        GPT分析失敗時のフォールバック
        """
        return {
            "overall_safety_score": 50,
            "risk_categories": {
                "violence": 10,
                "sexual_content": 10,
                "language": 10,
                "drugs": 10
            },
            "summary": f"自動分析に失敗しました。手動確認が必要です。{error_msg}",
            "key_concerns": ["分析エラー"],
            "positive_aspects": ["未評価"],
            "recommendation": "注意"
        }
    
    def calculate_final_score(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        最終的な安全性スコアとレコメンデーションの算出
        """
        score = analysis_result.get("overall_safety_score", 50)
        
        # スコアに基づく推奨レベル
        if score >= config.SCORE_THRESHOLDS["safe"]:
            recommendation = "推奨"
            status = "safe"
            icon = "✅"
        elif score >= config.SCORE_THRESHOLDS["caution"]:
            recommendation = "注意"
            status = "caution"
            icon = "⚠️"
        else:
            recommendation = "非推奨"
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
        最終的な安全性レポートの生成
        """
        safety_analysis = self.calculate_final_score(analysis_result)
        
        # キーワード抽出
        summary_text = safety_analysis.get("summary", "")
        keywords = []
        
        # 基本的なキーワード抽出（改善可能）
        common_words = ["教育", "学習", "楽しい", "面白い", "実験", "工作", "音楽", "歌", "ダンス"]
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
            "keywords": keywords[:10],  # 最大10個
            "processing_timestamp": None,  # 後で設定
            "version": "prototype-v1.0"
        }

if __name__ == "__main__":
    # テスト用
    scorer = SafetyScorer()
    
    # テスト用のダミーデータ
    test_scenes = [
        {"scene_number": 1, "visual_analysis": "明るい教室で子供たちが勉強している様子"},
        {"scene_number": 2, "visual_analysis": "先生が黒板で数学を教えている"}
    ]
    
    test_audio = [
        {"text": "今日は算数の勉強をしましょう"},
        {"text": "みんなで一緒に計算してみよう"}
    ]
    
    analysis = scorer.analyze_content_with_gpt(test_scenes, test_audio)
    final_report = scorer.generate_safety_report({"title": "テスト動画", "duration": 300}, analysis)
    
    print("Safety Analysis Test:")
    print(f"Score: {final_report['safety_analysis']['final_score']}")
    print(f"Recommendation: {final_report['safety_analysis']['final_recommendation']}")
    print(f"Summary: {final_report['safety_analysis']['summary']}")