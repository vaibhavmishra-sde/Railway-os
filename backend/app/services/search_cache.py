"""Cache-key helpers for the journey-search read-through cache."""

from datetime import date

from app.models.train import SeatClass


def journey_cache_key(
    service_date: date,
    origin: str,
    destination: str,
    seat_class: SeatClass | None,
    sort: str,
    descending: bool,
    offset: int,
    limit: int,
) -> str:
    """Return the canonical key for one fully qualified search request."""
    requested_class = seat_class.value if seat_class else "all"
    normalized_origin = origin.strip().upper()
    normalized_destination = destination.strip().upper()
    return (
        f"journeys:{service_date.isoformat()}:{normalized_origin}:{normalized_destination}"
        f":{requested_class}:{sort}:{str(descending).lower()}:{offset}:{limit}"
    )
