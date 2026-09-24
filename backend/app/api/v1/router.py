from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.routes import router as routes_router
from app.api.v1.stations import router as stations_router
from app.api.v1.trains import router as trains_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(stations_router)
api_router.include_router(trains_router)
api_router.include_router(routes_router)
