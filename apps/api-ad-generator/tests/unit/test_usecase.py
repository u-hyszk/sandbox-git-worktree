"""ユースケースのユニットテスト."""

from unittest.mock import AsyncMock, Mock
import pytest

from app.application.usecases import GenerateAdCopyUseCase
from app.domain.entities import AdCopy, AdInput, Tone
from app.domain.exceptions import AdGenerationError, InvalidInputError


class TestGenerateAdCopyUseCase:
    """GenerateAdCopyUseCaseのテスト."""

    def setup_method(self) -> None:
        """テスト前の準備."""
        self.mock_repository = Mock()
        self.usecase = GenerateAdCopyUseCase(self.mock_repository)

    @pytest.mark.asyncio
    async def test_successful_generation(self) -> None:
        """正常に広告文が生成されることをテストする."""
        # Arrange
        ad_input = AdInput(
            product_name="Test Product",
            target_audience="20代女性",
            appeal_points=["ポイント1", "ポイント2"],
            tone=Tone.CASUAL,
            num_copies=2,
        )
        
        expected_ad_copies = [
            AdCopy(copy_text="広告文1"),
            AdCopy(copy_text="広告文2"),
        ]
        
        self.mock_repository.generate_ad_copies = AsyncMock(return_value=expected_ad_copies)
        
        # Act
        result = await self.usecase.execute(ad_input)
        
        # Assert
        assert result == expected_ad_copies
        self.mock_repository.generate_ad_copies.assert_called_once_with(ad_input)

    @pytest.mark.asyncio
    async def test_empty_result_raises_error(self) -> None:
        """空の結果でエラーが発生することをテストする."""
        # Arrange
        ad_input = AdInput(
            product_name="Test Product",
            target_audience="20代女性",
            appeal_points=["ポイント1"],
        )
        
        self.mock_repository.generate_ad_copies = AsyncMock(return_value=[])
        
        # Act & Assert
        with pytest.raises(AdGenerationError, match="広告文の生成に失敗しました"):
            await self.usecase.execute(ad_input)

    @pytest.mark.asyncio
    async def test_repository_exception_raises_ad_generation_error(self) -> None:
        """リポジトリでの例外がAdGenerationErrorに変換されることをテストする."""
        # Arrange
        ad_input = AdInput(
            product_name="Test Product",
            target_audience="20代女性",
            appeal_points=["ポイント1"],
        )
        
        self.mock_repository.generate_ad_copies = AsyncMock(side_effect=Exception("API Error"))
        
        # Act & Assert
        with pytest.raises(AdGenerationError, match="広告文生成中にエラーが発生しました"):
            await self.usecase.execute(ad_input)