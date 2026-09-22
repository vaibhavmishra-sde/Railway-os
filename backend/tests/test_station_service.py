"""Tests for station domain behavior."""

import pytest

from app.api.v1.schemas import StationCreate
from app.services.station import StationCodeAlreadyExistsError, create_station


def test_create_station_persists_normalized_code(db_session) -> None:
    station = create_station(
        db_session,
        StationCreate(code="ndls", name="New Delhi", city="Delhi", state="Delhi"),
    )

    assert station.id
    assert station.code == "NDLS"


def test_create_station_rejects_duplicate_code(db_session) -> None:
    payload = StationCreate(code="NDLS", name="New Delhi", city="Delhi", state="Delhi")
    create_station(db_session, payload)

    with pytest.raises(StationCodeAlreadyExistsError):
        create_station(db_session, payload)
