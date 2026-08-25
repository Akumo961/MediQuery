"""Privacy-preserving in-process metrics for local operation and test environments.

Production deployments should replace this with a managed telemetry exporter that
enforces the same rule: never send report text, filenames, tokens, or email
addresses as metric dimensions.
"""

from collections import Counter
from threading import Lock
from time import perf_counter


class Metrics:
    def __init__(self) -> None:
        self._counts: Counter[str] = Counter()
        self._latency_ms: Counter[str] = Counter()
        self._lock = Lock()

    def increment(self, name: str) -> None:
        with self._lock:
            self._counts[name] += 1

    def observe_ms(self, name: str, elapsed_ms: float) -> None:
        with self._lock:
            self._counts[f"{name}.count"] += 1
            self._latency_ms[f"{name}.total"] += int(elapsed_ms)

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return {**dict(self._counts), **dict(self._latency_ms)}


metrics = Metrics()


def elapsed_ms(start: float) -> float:
    return (perf_counter() - start) * 1000
