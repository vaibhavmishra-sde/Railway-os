"""Validation tests for route API contracts."""

import pytest
from pydantic import ValidationError

from app.api.v1.schemas import RouteCreate, RouteStopCreate


def test_route_code_is_trimmed_and_uppercased() -> None:
    route = RouteCreate(code=" ndls-bct ", name="Capital Express", total_distance_km=1384)

    assert route.code == "NDLS-BCT"


@pytest.mark.parametrize("code", ["", "N D", "NDLS/BCT"])
def test_route_code_rejects_invalid_values(code: str) -> None:
    with pytest.raises(ValidationError):
        RouteCreate(code=code, name="Capital Express", total_distance_km=1384)


def test_route_stop_rejects_invalid_sequence_and_distance() -> None:
    with pytest.raises(ValidationError):
        RouteStopCreate(station_id="station-1", stop_sequence=0, distance_from_origin_km=-1)
