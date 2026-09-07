"""FastAPI application factory and ASGI entry point."""

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.metadata import API_PREFIX, APP_NAME, APP_VERSION


def create_app() -> FastAPI:
    """Create the RailwayOS API application."""
    application = FastAPI(title=APP_NAME, version=APP_VERSION)
    application.include_router(health_router)
    application.include_router(health_router, prefix=API_PREFIX)
    return application


app = create_app()
