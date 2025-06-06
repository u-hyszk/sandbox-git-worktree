"""API エンドポイントの統合テスト."""

from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.domain.entities import AdCopy


client = TestClient(app)


class TestGenerateAdCopyAPI:
    """広告文生成APIの統合テスト."""

    @patch("app.dependencies.get_settings")
    @patch("app.infrastructure.clients.claude_client.ClaudeAdGenerationRepository.generate_ad_copies")
    def test_successful_generation(self, mock_generate, mock_settings) -> None:
        """正常に広告文が生成されることをテストする."""
        # Arrange
        mock_settings.return_value.anthropic_api_key = "test_api_key"
        
        mock_ad_copies = [
            AdCopy(
                copy_text="素晴らしい商品です！",
                headline="魅力的なヘッドライン",
                call_to_action="今すぐ購入！",
            ),
            AdCopy(copy_text="もう一つの広告文"),
        ]
        
        mock_generate.return_value = mock_ad_copies
        
        request_data = {
            "productName": "Test Product",
            "targetAudience": "20代女性",
            "appealPoints": ["ポイント1", "ポイント2"],
            "tone": "casual",
            "numCopies": 2,
        }
        
        # Act
        response = client.post("/generate-ad-copy", json=request_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "generatedCopies" in data
        assert len(data["generatedCopies"]) == 2
        assert data["generatedCopies"][0]["copyText"] == "素晴らしい商品です！"
        assert data["generatedCopies"][0]["headline"] == "魅力的なヘッドライン"
        assert data["generatedCopies"][0]["callToAction"] == "今すぐ購入！"

    def test_invalid_request_returns_400(self) -> None:
        """無効なリクエストで400エラーが返されることをテストする."""
        # Arrange
        request_data = {
            "productName": "",  # 空の商品名
            "targetAudience": "20代女性",
            "appealPoints": ["ポイント1"],
        }
        
        # Act
        response = client.post("/generate-ad-copy", json=request_data)
        
        # Assert
        assert response.status_code == 400  # Domain validation error

    def test_missing_required_fields_returns_422(self) -> None:
        """必須フィールドが欠けている場合に422エラーが返されることをテストする."""
        # Arrange
        request_data = {
            "productName": "Test Product",
            # targetAudience と appealPoints が欠けている
        }
        
        # Act
        response = client.post("/generate-ad-copy", json=request_data)
        
        # Assert
        assert response.status_code == 422


def test_health_check() -> None:
    """ヘルスチェックエンドポイントのテスト."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI駆動型広告文生成API は正常に動作しています"}