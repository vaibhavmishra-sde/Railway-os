"""Deterministic synthetic-network fare calculations."""

from app.models.train import SeatClass

_CLASS_MULTIPLIERS: dict[SeatClass, float] = {
    SeatClass.GENERAL: 1.0,
    SeatClass.SLEEPER: 1.35,
    SeatClass.THIRD_AC: 2.1,
    SeatClass.SECOND_AC: 2.8,
    SeatClass.FIRST_AC: 4.2,
}


def calculate_fares(
    distance_km: float, classes: list[SeatClass]
) -> dict[SeatClass, int]:
    """Return stable whole-rupee fares for the requested route and classes."""
    base_fare = max(50, round(distance_km * 0.9))
    return {
        seat_class: round(base_fare * _CLASS_MULTIPLIERS[seat_class])
        for seat_class in classes
    }
