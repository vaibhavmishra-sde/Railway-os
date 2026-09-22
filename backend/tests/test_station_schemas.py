"""Validation tests for station API contracts."""

import pytest
from pydantic import ValidationError

from app.api.v1.schemas import StationCreate


def test_station_code_is_trimmed_and_uppercased() -> None:
    station = StationCreate(
        code=" ndls ", name="New Delhi", city="Delhi", state="Delhi"
    )

    assert station.code == "NDLS"
    assert station.timezone == "Asia/Kolkata"


@pytest.mark.parametrize("code", ["", "N D", "ND-LS"])
def test_station_code_rejects_invalid_values(code: str) -> None:
    with pytest.raises(ValidationError):
        StationCreate(code=code, name="New Delhi", city="Delhi", state="Delhi")
