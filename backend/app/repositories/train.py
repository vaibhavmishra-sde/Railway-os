"""Persistence operations for trains and coaches."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.train import Coach, Train


def get_train_by_number(session: Session, number: str) -> Train | None:
    return session.scalar(select(Train).where(Train.number == number))


def get_train(session: Session, train_id: str) -> Train | None:
    return session.get(Train, train_id)


def list_active_trains(session: Session, *, search: str | None = None, offset: int = 0, limit: int = 50) -> list[Train]:
    """Return active trains in numeric order."""
    statement = select(Train).where(Train.is_active)
    if search:
        pattern = f"%{search.strip()}%"
        statement = statement.where(Train.number.ilike(pattern) | Train.name.ilike(pattern))
    return list(session.scalars(statement.order_by(Train.number).offset(offset).limit(limit)))


def list_coaches(session: Session, train_id: str) -> list[Coach]:
    statement = (
        select(Coach).where(Coach.train_id == train_id).order_by(Coach.coach_number)
    )
    return list(session.scalars(statement))


def create_train(session: Session, *, number: str, name: str) -> Train:
    train = Train(number=number, name=name)
    session.add(train)
    session.commit()
    session.refresh(train)
    return train


def create_coach(session: Session, **coach_data: object) -> Coach:
    coach = Coach(**coach_data)
    session.add(coach)
    session.commit()
    session.refresh(coach)
    return coach
