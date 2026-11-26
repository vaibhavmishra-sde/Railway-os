"""Collision-aware PNR generation for synthetic RailwayOS bookings."""

import secrets
from collections.abc import Callable

PNR_PREFIX = "RO"
PNR_DIGITS = 8
MAX_GENERATION_ATTEMPTS = 10


class PNRGenerationError(RuntimeError):
    """Raised when a unique PNR cannot be generated within the retry budget."""


def format_pnr(number: int) -> str:
    """Format a numeric suffix as the ten-character RailwayOS PNR."""
    if not 0 <= number < 10**PNR_DIGITS:
        raise ValueError("PNR number must fit eight digits")
    return f"{PNR_PREFIX}{number:0{PNR_DIGITS}d}"


def generate_pnr(
    is_available: Callable[[str], bool],
    *,
    number_factory: Callable[[], int] | None = None,
    max_attempts: int = MAX_GENERATION_ATTEMPTS,
) -> str:
    """Return an unused PNR, retrying candidates that already exist.

    The database unique constraint remains the final concurrency guard; this
    check avoids ordinary collisions before a booking insert is attempted.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    next_number = number_factory or (lambda: secrets.randbelow(10**PNR_DIGITS))
    for _ in range(max_attempts):
        candidate = format_pnr(next_number())
        if is_available(candidate):
            return candidate
    raise PNRGenerationError("Unable to generate a unique PNR after retrying")
