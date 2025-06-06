"""FastAPI API for Ad Generator."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import get_settings
from app.infrastructure.api.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for Ad Generator",
)

# CORS-middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)


@app.get("/")
async def root() -> dict[str, str]:
    """API for Ad Generator."""
    return {"message": "AI駆動型広告文生成API は正常に動作しています"}