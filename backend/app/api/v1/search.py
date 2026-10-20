"""Direct journey search over dated train-service timetables."""

from datetime import date, datetime, time
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.v1.schemas import (
    JourneySearchResponse,
    JourneySearchResult,
    JourneySearchStop,
)
from app.db.session import get_db
from app.models.service import ServiceStop, TrainService
from app.models.station import Station
from app.models.train import SeatClass, Train
from app.services.fare import calculate_fares

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/journeys", response_model=JourneySearchResponse)
def search_journeys(
    origin: str = Query(..., min_length=2, max_length=10),
    destination: str = Query(..., min_length=2, max_length=10),
    service_date: date = Query(...),  # noqa: B008
    seat_class: SeatClass | None = Query(None),  # noqa: B008
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    sort: Literal["departure", "duration", "fare"] = Query("departure"),
    descending: bool = Query(False),
    db: Session = Depends(get_db),  # noqa: B008
) -> JourneySearchResponse:
    """Find direct services whose ordered stops contain both stations."""
    normalized_origin = origin.strip().upper()
    normalized_destination = destination.strip().upper()
    if normalized_origin == normalized_destination:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Origin and destination must differ"
        )

    stations = db.scalars(
        select(Station).where(
            Station.code.in_([normalized_origin, normalized_destination])
        )
    ).all()
    station_by_code = {station.code: station for station in stations}
    missing = (
        normalized_origin
        if normalized_origin not in station_by_code
        else normalized_destination
        if normalized_destination not in station_by_code
        else None
    )
    if missing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Unknown station: {missing}")

    services = (
        db.scalars(
            select(TrainService)
            .options(
                joinedload(TrainService.train).joinedload(Train.coaches),
                joinedload(TrainService.route),
                joinedload(TrainService.service_stops).joinedload(ServiceStop.station),
            )
            .where(TrainService.service_date == service_date)
        )
        .unique()
        .all()
    )
    matches: list[JourneySearchResult] = []
    for service in services:
        if seat_class and not any(
            coach.seat_class == seat_class for coach in service.train.coaches
        ):
            continue
        stops = {stop.station.code: stop for stop in service.service_stops}
        origin_stop, destination_stop = (
            stops.get(normalized_origin),
            stops.get(normalized_destination),
        )
        if (
            not origin_stop
            or not destination_stop
            or origin_stop.stop_sequence >= destination_stop.stop_sequence
        ):
            continue
        departure_time = (
            origin_stop.scheduled_departure or origin_stop.scheduled_arrival
        )
        arrival_time = (
            destination_stop.scheduled_arrival or destination_stop.scheduled_departure
        )
        duration_minutes = _duration_minutes(departure_time, arrival_time)
        available_classes = sorted(
            {coach.seat_class for coach in service.train.coaches},
            key=lambda item: item.value,
        )
        fares = calculate_fares(service.route.total_distance_km, available_classes)
        matches.append(
            JourneySearchResult(
                service_id=service.id,
                train_number=service.train.number,
                train_name=service.train.name,
                service_date=service.service_date,
                origin=JourneySearchStop(
                    station_code=normalized_origin,
                    station_name=origin_stop.station.name,
                    stop_sequence=origin_stop.stop_sequence,
                    scheduled_arrival=origin_stop.scheduled_arrival,
                    scheduled_departure=origin_stop.scheduled_departure,
                ),
                destination=JourneySearchStop(
                    station_code=normalized_destination,
                    station_name=destination_stop.station.name,
                    stop_sequence=destination_stop.stop_sequence,
                    scheduled_arrival=destination_stop.scheduled_arrival,
                    scheduled_departure=destination_stop.scheduled_departure,
                ),
                departure_time=departure_time,
                arrival_time=arrival_time,
                duration_minutes=duration_minutes,
                available_classes=available_classes,
                fares=fares,
            )
        )
    matches.sort(key=lambda item: _sort_key(item, sort), reverse=descending)
    return JourneySearchResponse(
        items=matches[offset : offset + limit],
        origin=normalized_origin,
        destination=normalized_destination,
        service_date=service_date,
        total=len(matches),
        offset=offset,
        limit=limit,
        sort=sort,
        descending=descending,
    )


def _duration_minutes(departure: time | None, arrival: time | None) -> int | None:
    """Calculate elapsed minutes, allowing a journey to cross midnight."""
    if departure is None or arrival is None:
        return None
    start = datetime.combine(date.min, departure)
    end = datetime.combine(date.min, arrival)
    if end < start:
        end = end.replace(day=end.day + 1)
    return int((end - start).total_seconds() // 60)


def _sort_key(result: JourneySearchResult, sort: str) -> tuple:
    """Build a total-order key so pagination remains deterministic."""
    if sort == "duration":
        primary = (
            result.duration_minutes if result.duration_minutes is not None else 10**9
        )
    elif sort == "fare":
        primary = min(result.fares.values(), default=10**9)
    else:
        primary = result.departure_time or result.arrival_time or time.max
    return primary, result.train_number, result.service_id
