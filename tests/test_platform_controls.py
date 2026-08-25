from src.core.rate_limit import FixedWindowRateLimiter
from src.core.observability import Metrics


def test_rate_limiter_blocks_after_window_limit() -> None:
    limiter = FixedWindowRateLimiter()
    assert limiter.allowed("test", limit=2, window_seconds=60)
    assert limiter.allowed("test", limit=2, window_seconds=60)
    assert not limiter.allowed("test", limit=2, window_seconds=60)


def test_metrics_never_require_sensitive_dimensions() -> None:
    local_metrics = Metrics()
    local_metrics.increment("reports.processed")
    local_metrics.observe_ms("api.request_latency", 4.8)
    assert local_metrics.snapshot() == {
        "reports.processed": 1,
        "api.request_latency.count": 1,
        "api.request_latency.total": 4,
    }
