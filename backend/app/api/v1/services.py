"""Dated train-service and timetable endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.schemas import (
    ServiceStopCreate,
    ServiceStopResponse,
    TrainServiceCreate,
    TrainServiceResponse,
)
from app.db.session import get_db
from app.repositories.service import get, list_by_date, list_stops
from app.services.service import (
    ServiceReferenceNotFoundError,
    TrainServiceAlreadyExistsError,
    add_stop,
    create_service,
)

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[TrainServiceResponse])
def list_services(
    service_date: date = Query(...),
    db: Session = Depends(get_db),  # noqa: B008
) -> list[TrainServiceResponse]:
    """List the scheduled train services for one calendar date."""
    return list_by_date(db, service_date)


@router.post(
    "", response_model=TrainServiceResponse, status_code=status.HTTP_201_CREATED
)
def create_service_endpoint(
    payload: TrainServiceCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> TrainServiceResponse:
    try:
        return create_service(db, payload)
    except TrainServiceAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
    except ServiceReferenceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/{service_id}/stops", response_model=list[ServiceStopResponse])
def get_service_stops(
    service_id: str,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[ServiceStopResponse]:
    if get(db, service_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    return list_stops(db, service_id)


@router.post(
    "/{service_id}/stops",
    response_model=ServiceStopResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_service_stop_endpoint(
    service_id: str,
    payload: ServiceStopCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> ServiceStopResponse:
    service = get(db, service_id)
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    try:
        return add_stop(db, service, payload)
    except ServiceReferenceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
