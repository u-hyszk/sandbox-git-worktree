"""Claude API クライアント実装."""

import json
from typing import List

import anthropic

from app.domain.entities import AdCopy, AdCopyEvaluation, AdInput
from app.domain.exceptions import AdGenerationError
from app.domain.repositories import AdGenerationRepository


class ClaudeAdGenerationRepository(AdGenerationRepository):
    """Claude API を使用した広告文生成リポジトリの実装."""

    def __init__(self, api_key: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)

    async def generate_ad_copies(self, ad_input: AdInput) -> List[AdCopy]:
        """Claude APIを使用して広告文を生成する."""
        try:
            prompt = self._build_prompt(ad_input)
            
            response = self._client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            return self._parse_response(content)
            
        except Exception as e:
            raise AdGenerationError(f"Claude APIでエラーが発生しました: {str(e)}") from e

    def _build_prompt(self, ad_input: AdInput) -> str:
        """広告文生成のためのプロンプトを構築する."""
        tone_description = ""
        if ad_input.tone:
            tone_description = f"トーン: {ad_input.tone.get_description()}"
        
        appeal_points_text = "\\n".join([f"- {point}" for point in ad_input.appeal_points])
        
        return f"""
あなたは広告文作成のプロフェッショナルです。以下の情報をもとに効果的な広告文を{ad_input.num_copies}つ作成してください。

商品・サービス名: {ad_input.product_name}
ターゲット層: {ad_input.target_audience}
アピールポイント:
{appeal_points_text}
{tone_description}

各広告文について以下の項目を含めて JSON 形式で出力してください：
- copyText: 広告文の本文（必須）
- headline: ヘッドライン（オプション）
- callToAction: 行動喚起メッセージ（オプション）
- evaluation: 評価情報（オプション）
  - relevanceScore: 関連性スコア（0.0-1.0）
  - creativityScore: 創造性スコア（0.0-1.0）
  - targetAudienceAppeal: ターゲット層への響きやすさコメント

出力形式例：
{{
  "adCopies": [
    {{
      "copyText": "広告文の内容",
      "headline": "魅力的なヘッドライン",
      "callToAction": "今すぐ行動！",
      "evaluation": {{
        "relevanceScore": 0.9,
        "creativityScore": 0.8,
        "targetAudienceAppeal": "コメント"
      }}
    }}
  ]
}}
"""

    def _parse_response(self, response_text: str) -> List[AdCopy]:
        """Claude APIのレスポンスをパースして AdCopy オブジェクトのリストに変換する."""
        try:
            # JSONの抽出を試行
            start_index = response_text.find("{")
            end_index = response_text.rfind("}") + 1
            
            if start_index == -1 or end_index == 0:
                raise ValueError("JSONが見つかりません")
            
            json_text = response_text[start_index:end_index]
            data = json.loads(json_text)
            
            ad_copies = []
            for item in data.get("adCopies", []):
                evaluation = None
                if "evaluation" in item and item["evaluation"]:
                    eval_data = item["evaluation"]
                    evaluation = AdCopyEvaluation(
                        relevance_score=eval_data.get("relevanceScore", 0.0),
                        creativity_score=eval_data.get("creativityScore", 0.0),
                        target_audience_appeal=eval_data.get("targetAudienceAppeal", "")
                    )
                
                ad_copy = AdCopy(
                    copy_text=item["copyText"],
                    headline=item.get("headline"),
                    call_to_action=item.get("callToAction"),
                    evaluation=evaluation
                )
                ad_copies.append(ad_copy)
            
            return ad_copies
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise AdGenerationError(f"レスポンスのパースに失敗しました: {str(e)}") from e