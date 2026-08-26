"""In-memory rate limiting and daily token budget."""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str) -> tuple[bool, int]:
        now = time.monotonic()
        cutoff = now - self.window_seconds

        with self._lock:
            hits = self._hits[key]
            while hits and hits[0] < cutoff:
                hits.popleft()

            if len(hits) >= self.max_requests:
                retry_after = int(hits[0] + self.window_seconds - now) + 1
                return False, max(retry_after, 1)

            hits.append(now)
            return True, 0


class TokenBudget:
    def __init__(self, daily_limit: int) -> None:
        self.daily_limit = daily_limit
        self._day = self._today()
        self._used = 0
        self._lock = threading.Lock()

    @staticmethod
    def _today() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _roll(self) -> None:
        today = self._today()
        if today != self._day:
            self._day = today
            self._used = 0

    def has_capacity(self) -> bool:
        with self._lock:
            self._roll()
            return self._used < self.daily_limit

    def record(self, tokens: int) -> None:
        with self._lock:
            self._roll()
            self._used += max(tokens, 0)
