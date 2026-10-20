from app.models.train import SeatClass
from app.services.fare import calculate_fares


def test_fares_are_deterministic_and_class_specific():
    assert calculate_fares(100, [SeatClass.SLEEPER, SeatClass.FIRST_AC]) == {
        SeatClass.SLEEPER: 122,
        SeatClass.FIRST_AC: 378,
    }


def test_short_routes_use_minimum_base_fare():
    assert calculate_fares(10, [SeatClass.GENERAL]) == {SeatClass.GENERAL: 50}


def test_empty_class_selection_returns_empty_fares():
    assert calculate_fares(100, []) == {}
