"""アプリケーション設定."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定クラス."""

    anthropic_api_key: str
    app_name: str = "AI駆動型広告文生成API"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"