"""Provider-neutral billing, entitlements, and usage metering.

This module deliberately does not fake payment processing. It provides the
server-side contract required for a future Stripe (or another provider)
adapter while keeping plan enforcement independent from the payment vendor.
Usage limits are evaluated per UTC calendar month.
"""

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.core.database import Subscription, UsageEvent, User


@dataclass(frozen=True)
class Plan:
    """A product plan and its server-enforced monthly entitlements."""

    name: str
    report_limit: int | None
    ai_request_limit: int | None


PLANS: dict[str, Plan] = {
    "free": Plan("free", report_limit=3, ai_request_limit=20),
    "pro": Plan("pro", report_limit=None, ai_request_limit=1000),
}


def _period_start() -> datetime:
    """Return the first instant of the current UTC calendar month."""
    now = datetime.now(timezone.utc)
    return datetime(now.year, now.month, 1, tzinfo=timezone.utc)


def _latest_subscription(db: Session, user_id: int) -> Subscription | None:
    """Return the newest subscription record for a user, if one exists."""
    return db.scalar(
        select(Subscription)
        .where(Subscription.user_id == user_id)
        .order_by(Subscription.created_at.desc())
    )


def get_plan(user: User, db: Session) -> Plan:
    subscription = _latest_subscription(db, user.id)
    if subscription and subscription.status == "active" and subscription.plan in PLANS:
        return PLANS[subscription.plan]
    return PLANS.get(user.plan, PLANS["free"])


def current_usage(db: Session, user_id: int, metric: str) -> int:
    return int(
        db.scalar(
            select(func.coalesce(func.sum(UsageEvent.quantity), 0)).where(
                UsageEvent.user_id == user_id,
                UsageEvent.metric == metric,
                UsageEvent.created_at >= _period_start(),
            )
        )
        or 0
    )


def can_consume(db: Session, user: User, metric: str, quantity: int = 1) -> bool:
    if quantity < 1:
        return False
    plan = get_plan(user, db)
    limit = {
        "report": plan.report_limit,
        "ai_request": plan.ai_request_limit,
    }.get(metric)
    if limit is None:
        return True
    return current_usage(db, user.id, metric) + quantity <= limit


def record_usage(
    db: Session,
    user: User,
    metric: str,
    quantity: int = 1,
    idempotency_key: str | None = None,
) -> bool:
    if quantity < 1:
        raise ValueError("usage quantity must be positive")
    if idempotency_key:
        existing = db.scalar(
            select(UsageEvent).where(UsageEvent.idempotency_key == idempotency_key)
        )
        if existing:
            return False
    if not can_consume(db, user, metric, quantity):
        return False
    db.add(
        UsageEvent(
            user_id=user.id,
            metric=metric,
            quantity=quantity,
            idempotency_key=idempotency_key,
        )
    )
    return True


def billing_summary(db: Session, user: User) -> dict[str, object]:
    plan = get_plan(user, db)
    subscription = _latest_subscription(db, user.id)
    return {
        "plan": plan.name,
        "subscription_status": subscription.status if subscription else "none",
        "reports": {
            "used": current_usage(db, user.id, "report"),
            "limit": plan.report_limit,
        },
        "ai_requests": {
            "used": current_usage(db, user.id, "ai_request"),
            "limit": plan.ai_request_limit,
        },
        "billing_provider": subscription.provider if subscription else None,
        "usage_period": _period_start().date().isoformat(),
    }
