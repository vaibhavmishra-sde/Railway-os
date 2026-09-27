"""Static catalog definitions for the Day 22 synthetic railway network."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StationSeed:
    code: str
    name: str
    city: str
    state: str


@dataclass(frozen=True, slots=True)
class RouteSeed:
    code: str
    name: str
    station_codes: tuple[str, ...]
    distance_km: float


@dataclass(frozen=True, slots=True)
class ServiceSeed:
    train_number: str
    route_code: str
    service_date: str


STATIONS: tuple[StationSeed, ...] = ()
ROUTES: tuple[RouteSeed, ...] = ()
SERVICES: tuple[ServiceSeed, ...] = ()
