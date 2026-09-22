"""Validation tests for train and coach contracts."""

import pytest
from pydantic import ValidationError

from app.api.v1.schemas import CoachCreate, TrainCreate
from app.models.train import SeatClass


def test_train_number_is_trimmed() -> None:
    assert TrainCreate(number=" 12301 ", name="Rajdhani").number == "12301"


@pytest.mark.parametrize("number", ["12A01", "12-301"])
def test_train_number_requires_digits(number: str) -> None:
    with pytest.raises(ValidationError):
        TrainCreate(number=number, name="Rajdhani")


def test_coach_schema_normalizes_number_and_parses_class() -> None:
    coach = CoachCreate(coach_number=" a1 ", seat_class="SECOND_AC", total_seats=48)
    assert coach.coach_number == "A1"
    assert coach.seat_class is SeatClass.SECOND_AC
