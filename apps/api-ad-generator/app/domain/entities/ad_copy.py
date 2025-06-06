"""生成された広告文を表すドメインエンティティ."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AdCopyEvaluation:
    """広告文の評価情報を保持するValue Object."""

    relevance_score: float
    creativity_score: float
    target_audience_appeal: str

    def __post_init__(self) -> None:
        """バリデーションロジック."""
        if not (0.0 <= self.relevance_score <= 1.0):
            raise ValueError("関連性スコアは0.0から1.0の間で指定してください")
        
        if not (0.0 <= self.creativity_score <= 1.0):
            raise ValueError("創造性スコアは0.0から1.0の間で指定してください")
        
        if not self.target_audience_appeal.strip():
            raise ValueError("ターゲット層への響きやすさコメントは必須です")


@dataclass(frozen=True)
class AdCopy:
    """生成された広告文を保持するエンティティ."""

    copy_text: str
    headline: Optional[str] = None
    call_to_action: Optional[str] = None
    evaluation: Optional[AdCopyEvaluation] = None

    def __post_init__(self) -> None:
        """バリデーションロジック."""
        if not self.copy_text.strip():
            raise ValueError("広告文の本文は必須です")