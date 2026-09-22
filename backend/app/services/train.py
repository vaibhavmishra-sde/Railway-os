"""Train and coach domain rules."""

from sqlalchemy.orm import Session

from app.api.v1.schemas import CoachCreate, TrainCreate
from app.models.train import Coach, Train
from app.repositories import train as train_repository


class TrainNumberAlreadyExistsError(ValueError):
    """Raised when a train number is already registered."""


def create_train(session: Session, payload: TrainCreate) -> Train:
    if train_repository.get_train_by_number(session, payload.number) is not None:
        raise TrainNumberAlreadyExistsError("A train with this number already exists")
    return train_repository.create_train(session, **payload.model_dump())


def add_coach(session: Session, train: Train, payload: CoachCreate) -> Coach:
    return train_repository.create_coach(
        session, train_id=train.id, **payload.model_dump()
    )
