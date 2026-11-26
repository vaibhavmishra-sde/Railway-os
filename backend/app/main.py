"""FastAPI application factory and ASGI entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.health import router as health_router
from app.core.config import settings
from app.core.metadata import API_PREFIX, APP_NAME, APP_VERSION


def create_app() -> FastAPI:
    """Create the RailwayOS API application."""
    application = FastAPI(title=APP_NAME, version=APP_VERSION)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL, "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )
    application.include_router(health_router)
    from app.api.v1.router import api_router

    application.include_router(api_router, prefix=API_PREFIX)
    return application


app = create_app()
