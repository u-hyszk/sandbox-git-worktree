"""広告文生成リポジトリのインターフェース."""

from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import AdCopy, AdInput


class AdGenerationRepository(ABC):
    """広告文生成のためのリポジトリインターフェース."""

    @abstractmethod
    async def generate_ad_copies(self, ad_input: AdInput) -> List[AdCopy]:
        """広告文を生成する.
        
        Args:
            ad_input: 広告文生成のための入力データ
            
        Returns:
            生成された広告文のリスト
            
        Raises:
            AdGenerationError: 広告文生成に失敗した場合
        """
        pass