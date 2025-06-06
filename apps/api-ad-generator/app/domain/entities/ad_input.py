"""広告生成のための入力データを表すドメインエンティティ."""

from dataclasses import dataclass
from typing import List, Optional

from app.domain.entities.tone import Tone


@dataclass(frozen=True)
class AdInput:
    """広告文生成のための入力情報を保持するエンティティ."""

    product_name: str
    target_audience: str
    appeal_points: List[str]
    tone: Optional[Tone] = None
    num_copies: int = 3

    def __post_init__(self) -> None:
        """バリデーションロジック."""
        if not self.product_name.strip():
            raise ValueError("商品名は必須です")
        
        if not self.target_audience.strip():
            raise ValueError("ターゲット層は必須です")
        
        if not self.appeal_points or len(self.appeal_points) == 0:
            raise ValueError("アピールポイントは最低1つ必要です")
        
        if any(not point.strip() for point in self.appeal_points):
            raise ValueError("アピールポイントは空文字を含むことはできません")
        
        if self.num_copies < 1 or self.num_copies > 5:
            raise ValueError("生成数は1から5の間で指定してください")