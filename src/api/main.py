"""FastAPI entrypoint for the MediQuery report-organizing service."""

from contextlib import asynccontextmanager
import os
from time import perf_counter
from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import uvicorn

from src.api.routes import auth, reports, search
from src.core.database import create_database
from src.core.observability import elapsed_ms, metrics
from src.core.rate_limit import rate_limiter
from src.core.settings import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize local development persistence before serving requests."""
    create_database()
    yield


app = FastAPI(
    title="MediQuery AI",
    description="Authenticated medical-report extraction and educational literature lookup.",
    version="2.0.0",
    lifespan=lifespan,
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])


@app.middleware("http")
async def security_headers(request: Request, call_next):
    request_id = uuid4().hex
    client_host = request.client.host if request.client else "unknown"
    if request.url.path.startswith("/api/") and not rate_limiter.allowed(
        f"api:{client_host}", limit=120, window_seconds=60
    ):
        metrics.increment("api.rate_limited")
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again shortly."},
            headers={"Retry-After": "60", "X-Request-ID": request_id},
        )
    started = perf_counter()
    response = await call_next(request)
    metrics.observe_ms("api.request_latency", elapsed_ms(started))
    metrics.increment(f"api.status.{response.status_code}")
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers[
        "Content-Security-Policy"
    ] = "default-src 'none'; frame-ancestors 'none'"
    if settings.environment.lower() == "production":
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"
    return response


@app.get("/")
async def root():
    """Return API metadata for simple connectivity checks."""
    return {
        "message": "MediQuery API",
        "version": "2.0.0",
        "endpoints": {
            "search": "/api/search",
            "authentication": "/api/auth",
            "reports": "/api/reports",
        },
    }


@app.get("/health")
async def health_check():
    """Return a cheap health signal for Docker and smoke tests."""
    return {"status": "healthy"}


@app.get("/health/metrics")
async def health_metrics():
    """Return aggregate, non-sensitive counters for an internal monitoring collector."""
    return {"metrics": metrics.snapshot()}


if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("DEBUG", "False").lower() == "true",
    )
