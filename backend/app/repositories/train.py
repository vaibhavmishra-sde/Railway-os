"""Persistence operations for trains and coaches."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.train import Coach, Train


def get_train_by_number(session: Session, number: str) -> Train | None:
    return session.scalar(select(Train).where(Train.number == number))


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
