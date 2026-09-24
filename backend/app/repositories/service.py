"""Persistence operations for dated train services and timetable stops."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service import ServiceStop, TrainService


def get(session: Session, service_id: str) -> TrainService | None:
    return session.get(TrainService, service_id)


def get_by_train_and_date(
    session: Session, train_id: str, service_date: date
) -> TrainService | None:
    return session.scalar(
        select(TrainService).where(
            TrainService.train_id == train_id,
            TrainService.service_date == service_date,
        )
    )


def list_by_date(session: Session, service_date: date) -> list[TrainService]:
    return list(
        session.scalars(
            select(TrainService)
            .where(TrainService.service_date == service_date)
            .order_by(TrainService.train_id)
        )
    )


def list_stops(session: Session, service_id: str) -> list[ServiceStop]:
    return list(
        session.scalars(
            select(ServiceStop)
            .where(ServiceStop.service_id == service_id)
            .order_by(ServiceStop.stop_sequence)
        )
    )


def create(session: Session, **service_data: object) -> TrainService:
    service = TrainService(**service_data)
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def create_stop(session: Session, **stop_data: object) -> ServiceStop:
    stop = ServiceStop(**stop_data)
    session.add(stop)
    session.commit()
    session.refresh(stop)
    return stop
