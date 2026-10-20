from datetime import date

from app.models.train import SeatClass
from app.services.search_cache import journey_cache_key


def test_journey_cache_key_is_canonical():
    assert (
        journey_cache_key(
            date(2026, 10, 21), "ndls", "bct", SeatClass.SLEEPER, "fare", True, 10, 20
        )
        == "journeys:2026-10-21:NDLS:BCT:SLEEPER:fare:true:10:20"
    )


def test_journey_cache_key_distinguishes_all_classes():
    assert journey_cache_key(
        date(2026, 10, 21), "NDLS", "BCT", None, "departure", False, 0, 50
    ).endswith(":all:departure:false:0:50")
