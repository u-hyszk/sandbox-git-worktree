"""FastAPI のリクエスト・レスポンスモデル定義."""

from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from app.domain.entities import Tone


class AdCopyGenerationRequest(BaseModel):
    """広告文生成リクエストモデル."""
    
    model_config = ConfigDict(populate_by_name=True)

    product_name: str = Field(..., alias="productName", description="広告を作成する商品またはサービスの名称")
    target_audience: str = Field(..., alias="targetAudience", description="広告のターゲットとなる顧客層")
    appeal_points: List[str] = Field(..., alias="appealPoints", description="商品/サービスの主なアピールポイント（複数可）")
    tone: Optional[Tone] = Field(Tone.PROFESSIONAL, description="広告文のトーン")
    num_copies: int = Field(3, alias="numCopies", ge=1, le=5, description="生成する広告文の候補数")


class AdCopyEvaluationResponse(BaseModel):
    """広告文評価レスポンスモデル."""
    
    model_config = ConfigDict(populate_by_name=True)

    relevance_score: float = Field(..., alias="relevanceScore", description="入力情報との関連性スコア (0.0 - 1.0)")
    creativity_score: float = Field(..., alias="creativityScore", description="広告文の創造性スコア (0.0 - 1.0)")
    target_audience_appeal: str = Field(..., alias="targetAudienceAppeal", description="ターゲット層への響きやすさコメント")


class GeneratedAdCopyResponse(BaseModel):
    """生成された広告文レスポンスモデル."""
    
    model_config = ConfigDict(populate_by_name=True)

    copy_text: str = Field(..., alias="copyText", description="生成された広告文の本文")
    headline: Optional[str] = Field(None, description="広告のヘッドライン（見出し）")
    call_to_action: Optional[str] = Field(None, alias="callToAction", description="行動喚起のメッセージ")
    evaluation: Optional[AdCopyEvaluationResponse] = Field(None, description="広告文の評価情報")


class AdCopyGenerationResponse(BaseModel):
    """広告文生成レスポンスモデル."""
    
    model_config = ConfigDict(populate_by_name=True)

    generated_copies: List[GeneratedAdCopyResponse] = Field(..., alias="generatedCopies", description="生成された広告文の候補リスト")


class ErrorResponse(BaseModel):
    """エラーレスポンスモデル."""

    message: str = Field(..., description="エラーメッセージ")
    code: str = Field(..., description="エラーコード")