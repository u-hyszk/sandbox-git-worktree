"""ドメインエンティティのユニットテスト."""

import pytest

from app.domain.entities import AdCopy, AdCopyEvaluation, AdInput, Tone


class TestAdInput:
    """AdInputエンティティのテスト."""

    def test_valid_ad_input(self) -> None:
        """正常なAdInputの作成をテストする."""
        ad_input = AdInput(
            product_name="Test Product",
            target_audience="20代女性",
            appeal_points=["ポイント1", "ポイント2"],
            tone=Tone.CASUAL,
            num_copies=2,
        )
        
        assert ad_input.product_name == "Test Product"
        assert ad_input.target_audience == "20代女性"
        assert ad_input.appeal_points == ["ポイント1", "ポイント2"]
        assert ad_input.tone == Tone.CASUAL
        assert ad_input.num_copies == 2

    def test_empty_product_name_raises_error(self) -> None:
        """空の商品名でエラーが発生することをテストする."""
        with pytest.raises(ValueError, match="商品名は必須です"):
            AdInput(
                product_name="",
                target_audience="20代女性",
                appeal_points=["ポイント1"],
            )

    def test_empty_target_audience_raises_error(self) -> None:
        """空のターゲット層でエラーが発生することをテストする."""
        with pytest.raises(ValueError, match="ターゲット層は必須です"):
            AdInput(
                product_name="Test Product",
                target_audience="",
                appeal_points=["ポイント1"],
            )

    def test_empty_appeal_points_raises_error(self) -> None:
        """空のアピールポイントでエラーが発生することをテストする."""
        with pytest.raises(ValueError, match="アピールポイントは最低1つ必要です"):
            AdInput(
                product_name="Test Product",
                target_audience="20代女性",
                appeal_points=[],
            )

    def test_invalid_num_copies_raises_error(self) -> None:
        """無効な生成数でエラーが発生することをテストする."""
        with pytest.raises(ValueError, match="生成数は1から5の間で指定してください"):
            AdInput(
                product_name="Test Product",
                target_audience="20代女性",
                appeal_points=["ポイント1"],
                num_copies=0,
            )

        with pytest.raises(ValueError, match="生成数は1から5の間で指定してください"):
            AdInput(
                product_name="Test Product",
                target_audience="20代女性",
                appeal_points=["ポイント1"],
                num_copies=6,
            )


class TestAdCopyEvaluation:
    """AdCopyEvaluationエンティティのテスト."""

    def test_valid_evaluation(self) -> None:
        """正常なAdCopyEvaluationの作成をテストする."""
        evaluation = AdCopyEvaluation(
            relevance_score=0.9,
            creativity_score=0.8,
            target_audience_appeal="良い響き",
        )
        
        assert evaluation.relevance_score == 0.9
        assert evaluation.creativity_score == 0.8
        assert evaluation.target_audience_appeal == "良い響き"

    def test_invalid_relevance_score_raises_error(self) -> None:
        """無効な関連性スコアでエラーが発生することをテストする."""
        with pytest.raises(ValueError, match="関連性スコアは0.0から1.0の間で指定してください"):
            AdCopyEvaluation(
                relevance_score=1.5,
                creativity_score=0.8,
                target_audience_appeal="良い響き",
            )

    def test_invalid_creativity_score_raises_error(self) -> None:
        """無効な創造性スコアでエラーが発生することをテストする."""
        with pytest.raises(ValueError, match="創造性スコアは0.0から1.0の間で指定してください"):
            AdCopyEvaluation(
                relevance_score=0.9,
                creativity_score=-0.1,
                target_audience_appeal="良い響き",
            )


class TestAdCopy:
    """AdCopyエンティティのテスト."""

    def test_valid_ad_copy(self) -> None:
        """正常なAdCopyの作成をテストする."""
        evaluation = AdCopyEvaluation(
            relevance_score=0.9,
            creativity_score=0.8,
            target_audience_appeal="良い響き",
        )
        
        ad_copy = AdCopy(
            copy_text="素晴らしい商品です",
            headline="魅力的なヘッドライン",
            call_to_action="今すぐ購入！",
            evaluation=evaluation,
        )
        
        assert ad_copy.copy_text == "素晴らしい商品です"
        assert ad_copy.headline == "魅力的なヘッドライン"
        assert ad_copy.call_to_action == "今すぐ購入！"
        assert ad_copy.evaluation == evaluation

    def test_empty_copy_text_raises_error(self) -> None:
        """空の広告文でエラーが発生することをテストする."""
        with pytest.raises(ValueError, match="広告文の本文は必須です"):
            AdCopy(copy_text="")


class TestTone:
    """Toneエンティティのテスト."""

    def test_tone_descriptions(self) -> None:
        """各トーンの説明を取得できることをテストする."""
        assert Tone.FORMAL.get_description() == "丁寧で格式のある表現"
        assert Tone.CASUAL.get_description() == "親しみやすく気軽な表現"
        assert Tone.HUMOROUS.get_description() == "ユーモアを交えた表現"
        assert Tone.PROFESSIONAL.get_description() == "専門的で信頼感のある表現"
        assert Tone.FRIENDLY.get_description() == "フレンドリーで親近感のある表現"