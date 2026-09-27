"""Static catalog definitions for the Day 22 synthetic railway network."""

from dataclasses import dataclass
from datetime import date


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


STATIONS: tuple[StationSeed, ...] = (
    StationSeed("NCR", "North City Central", "North City", "Northland"),
    StationSeed("RIV", "Riverside Junction", "Riverside", "Northland"),
    StationSeed("HIL", "Hillview", "Hillview", "Northland"),
    StationSeed("LAK", "Lake Town", "Lake Town", "Centralia"),
    StationSeed("MKT", "Market Square", "Market City", "Centralia"),
    StationSeed("GRN", "Greenfield", "Greenfield", "Centralia"),
    StationSeed("CRS", "Crossroads", "Crossroads", "Centralia"),
    StationSeed("SUN", "Sunport", "Sunport", "Southland"),
    StationSeed("BAY", "Bayview", "Bayview", "Southland"),
    StationSeed("PAL", "Palmgrove", "Palmgrove", "Southland"),
    StationSeed("HBR", "Harbor Central", "Harbor City", "Southland"),
    StationSeed("CST", "Coastal Terminal", "Coastal City", "Southland"),
)
ROUTES: tuple[RouteSeed, ...] = (
    RouteSeed("NCR-CST", "North City to Coastal Terminal", ("NCR", "RIV", "HIL", "LAK", "MKT", "GRN", "CRS", "SUN", "BAY", "PAL", "HBR", "CST"), 842.0),
    RouteSeed("NCR-HBR", "North City to Harbor Central", ("NCR", "RIV", "HIL", "LAK", "MKT", "GRN", "CRS", "SUN", "BAY", "PAL", "HBR"), 798.0),
    RouteSeed("RIV-CST", "Riverside to Coastal Terminal", ("RIV", "HIL", "LAK", "MKT", "GRN", "CRS", "SUN", "BAY", "PAL", "HBR", "CST"), 770.0),
)
SERVICES: tuple[ServiceSeed, ...] = (
    ServiceSeed("12001", "NCR-CST", "2026-10-01"),
    ServiceSeed("12002", "NCR-CST", "2026-10-01"),
    ServiceSeed("12003", "NCR-HBR", "2026-10-01"),
    ServiceSeed("12004", "RIV-CST", "2026-10-02"),
    ServiceSeed("12005", "NCR-CST", "2026-10-02"),
)


def validate_catalog() -> None:
    """Raise ``ValueError`` when catalog references or invariants are invalid."""
    station_codes = {station.code for station in STATIONS}
    if len(station_codes) != len(STATIONS):
        raise ValueError("station codes must be unique")
    route_codes = {route.code for route in ROUTES}
    if len(route_codes) != len(ROUTES):
        raise ValueError("route codes must be unique")
    for route in ROUTES:
        if len(route.station_codes) < 3:
            raise ValueError(f"route {route.code} needs at least three stations")
        if not set(route.station_codes) <= station_codes:
            raise ValueError(f"route {route.code} references an unknown station")
        if route.distance_km <= 0:
            raise ValueError(f"route {route.code} must have positive distance")
    for service in SERVICES:
        if service.route_code not in route_codes:
            raise ValueError(f"service {service.train_number} references an unknown route")
        try:
            date.fromisoformat(service.service_date)
        except ValueError as exc:
            raise ValueError(f"service {service.train_number} has an invalid date") from exc
