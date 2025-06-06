"""�X'�en-�."""

from functools import lru_cache

from fastapi import Depends

from app.application.usecases import GenerateAdCopyUseCase
from app.domain.repositories import AdGenerationRepository
from app.infrastructure.clients.claude_client import ClaudeAdGenerationRepository
from app.infrastructure.config.settings import Settings


@lru_cache()
def get_settings() -> Settings:
    """Get settings."""
    return Settings()


def get_ad_generation_repository(
    settings: Settings = Depends(get_settings),
) -> AdGenerationRepository:
    """Get ad generation repository."""
    return ClaudeAdGenerationRepository(api_key=settings.anthropic_api_key)


def get_generate_ad_copy_usecase(
    repository: AdGenerationRepository = Depends(get_ad_generation_repository),
) -> GenerateAdCopyUseCase:
    """Get generate ad copy usecase."""
    return GenerateAdCopyUseCase(ad_generation_repository=repository)