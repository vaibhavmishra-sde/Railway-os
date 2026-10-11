"""Small process-local rate limiter for sensitive endpoints."""

from collections import defaultdict
from time import monotonic


class LoginRateLimiter:
    def __init__(self, max_attempts: int, window_seconds: int) -> None:
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = monotonic()
        recent = [
            timestamp
            for timestamp in self._attempts[key]
            if now - timestamp < self.window_seconds
        ]
        self._attempts[key] = recent
        if len(recent) >= self.max_attempts:
            return False
        recent.append(now)
        return True

    def clear(self) -> None:
        self._attempts.clear()
