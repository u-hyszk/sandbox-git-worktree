"""広告文生成ユースケース."""

from typing import List

from app.domain.entities import AdCopy, AdInput
from app.domain.exceptions import AdGenerationError, InvalidInputError
from app.domain.repositories import AdGenerationRepository


class GenerateAdCopyUseCase:
    """広告文生成ユースケース."""

    def __init__(self, ad_generation_repository: AdGenerationRepository) -> None:
        self._ad_generation_repository = ad_generation_repository

    async def execute(self, ad_input: AdInput) -> List[AdCopy]:
        """広告文生成を実行する.
        
        Args:
            ad_input: 広告文生成のための入力データ
            
        Returns:
            生成された広告文のリスト
            
        Raises:
            InvalidInputError: 入力データが不正な場合
            AdGenerationError: 広告文生成に失敗した場合
        """
        try:
            # 入力データのバリデーションは既にエンティティで実施済み
            ad_copies = await self._ad_generation_repository.generate_ad_copies(ad_input)
            
            if not ad_copies:
                raise AdGenerationError("広告文の生成に失敗しました")
            
            return ad_copies
            
        except ValueError as e:
            raise InvalidInputError(str(e)) from e
        except Exception as e:
            raise AdGenerationError(f"広告文生成中にエラーが発生しました: {str(e)}") from e