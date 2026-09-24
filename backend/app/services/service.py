"""Train-service domain rules."""

from sqlalchemy.orm import Session

from app.api.v1.schemas import ServiceStopCreate, TrainServiceCreate
from app.models.service import ServiceStop, TrainService
from app.models.station import Station
from app.models.train import Train
from app.repositories import route as route_repository
from app.repositories import service as service_repository


class TrainServiceAlreadyExistsError(ValueError):
    """Raised when a train already has a service on the supplied date."""


class ServiceReferenceNotFoundError(ValueError):
    """Raised when a service references a train, route, or station that is absent."""


def create_service(session: Session, payload: TrainServiceCreate) -> TrainService:
    if session.get(Train, payload.train_id) is None:
        raise ServiceReferenceNotFoundError("Train not found")
    if route_repository.get(session, payload.route_id) is None:
        raise ServiceReferenceNotFoundError("Route not found")
    if service_repository.get_by_train_and_date(
        session, payload.train_id, payload.service_date
    ) is not None:
        raise TrainServiceAlreadyExistsError(
            "This train already has a service on the selected date"
        )
    return service_repository.create(session, **payload.model_dump())


def add_stop(
    session: Session, service: TrainService, payload: ServiceStopCreate
) -> ServiceStop:
    if session.get(Station, payload.station_id) is None:
        raise ServiceReferenceNotFoundError("Station not found")
    return service_repository.create_stop(
        session, service_id=service.id, **payload.model_dump()
    )
