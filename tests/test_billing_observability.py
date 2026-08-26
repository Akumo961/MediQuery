from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from src.api.main import app
from src.core.billing import PLANS, can_consume, current_usage, record_usage
from src.core.database import SessionLocal, User


def test_plan_definitions_are_explicit_and_provider_neutral() -> None:
    assert PLANS["free"].report_limit == 3
    assert PLANS["free"].ai_request_limit == 20
    assert PLANS["pro"].report_limit is None
    assert PLANS["pro"].ai_request_limit == 1000


def test_usage_meter_is_idempotent_and_enforces_limit() -> None:
    db = SessionLocal()
    try:
        user = User(email=f"meter-{uuid4().hex}@example.test", password_hash="test")
        db.add(user)
        db.commit()
        db.refresh(user)
        for index in range(20):
            assert record_usage(db, user, "ai_request", idempotency_key=f"test:{user.id}:{index}")
        db.commit()
        assert current_usage(db, user.id, "ai_request") == 20
        assert not can_consume(db, user, "ai_request")
        assert not record_usage(db, user, "ai_request", idempotency_key=f"test:{user.id}:blocked")
        assert not record_usage(db, user, "ai_request", idempotency_key=f"test:{user.id}:0")
    finally:
        db.rollback()
        db.delete(db.scalar(select(User).where(User.email == user.email)))
        db.commit()
        db.close()


def test_billing_summary_requires_authentication() -> None:
    with TestClient(app) as client:
        assert client.get("/api/billing/summary").status_code == 401


def test_billing_summary_and_checkout_are_honest_when_provider_is_unconfigured() -> None:
    with TestClient(app) as client:
        email = f"billing-{uuid4().hex}@example.test"
        token = client.post(
            "/api/auth/signup",
            json={
                "email": email,
                "password": "a-long-enough-password",
                "acknowledge_medical_limitations": True,
            },
        ).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        summary = client.get("/api/billing/summary", headers=headers)
        assert summary.status_code == 200
        assert summary.json()["plan"] == "free"
        checkout = client.post("/api/billing/checkout", headers=headers)
        assert checkout.status_code == 200
        assert checkout.json()["available"] is False
        assert checkout.json()["checkout_url"] is None


def test_metrics_endpoint_is_not_public() -> None:
    with TestClient(app) as client:
        response = client.get("/health/metrics")
        assert response.status_code == 404
