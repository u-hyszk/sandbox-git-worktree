"""広告文のトーンを表すValue Object."""

from enum import Enum


class Tone(str, Enum):
    """広告文のトーンを表す列挙型."""

    FORMAL = "formal"
    CASUAL = "casual"
    HUMOROUS = "humorous"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"

    def get_description(self) -> str:
        """トーンの説明を取得."""
        descriptions = {
            self.FORMAL: "丁寧で格式のある表現",
            self.CASUAL: "親しみやすく気軽な表現",
            self.HUMOROUS: "ユーモアを交えた表現",
            self.PROFESSIONAL: "専門的で信頼感のある表現",
            self.FRIENDLY: "フレンドリーで親近感のある表現",
        }
        return descriptions[self]