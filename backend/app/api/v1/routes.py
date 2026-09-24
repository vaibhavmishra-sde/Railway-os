"""Public synthetic route endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.schemas import (
    RouteCreate,
    RouteResponse,
    RouteStopCreate,
    RouteStopResponse,
)
from app.db.session import get_db
from app.repositories.route import get, list_active, list_stops
from app.services.route import (
    RouteCodeAlreadyExistsError,
    RouteStopStationNotFoundError,
    add_stop,
    create_route,
)

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("", response_model=list[RouteResponse])
def list_routes(db: Session = Depends(get_db)) -> list[RouteResponse]:  # noqa: B008
    return list_active(db)


@router.post("", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route_endpoint(
    payload: RouteCreate, db: Session = Depends(get_db)  # noqa: B008
) -> RouteResponse:
    try:
        return create_route(db, payload)
    except RouteCodeAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/{route_id}/stops", response_model=list[RouteStopResponse])
def get_route_stops(
    route_id: str, db: Session = Depends(get_db)  # noqa: B008
) -> list[RouteStopResponse]:
    if get(db, route_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return list_stops(db, route_id)


@router.post(
    "/{route_id}/stops",
    response_model=RouteStopResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_route_stop_endpoint(
    route_id: str,
    payload: RouteStopCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> RouteStopResponse:
    route = get(db, route_id)
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    try:
        return add_stop(db, route, payload)
    except RouteStopStationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
