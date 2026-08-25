"""Small fixed-window limiter for one-process deployments.

Use an atomic Redis/provider-backed limiter before horizontally scaling.
"""

from collections import defaultdict, deque
from threading import Lock
from time import monotonic


class FixedWindowRateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allowed(self, key: str, limit: int, window_seconds: int) -> bool:
        now = monotonic()
        with self._lock:
            history = self._hits[key]
            cutoff = now - window_seconds
            while history and history[0] <= cutoff:
                history.popleft()
            if len(history) >= limit:
                return False
            history.append(now)
            return True


rate_limiter = FixedWindowRateLimiter()
