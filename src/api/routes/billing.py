"""Authenticated billing and entitlement endpoints.

Payment execution is intentionally provider-neutral. A real checkout provider
must be configured before an upgrade URL is returned; the API never fabricates
successful payment state.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies import current_user
from src.api.schemas import BillingResponse, CheckoutResponse
from src.core.billing import billing_summary
from src.core.database import User, get_db
from src.core.observability import metrics
from src.core.settings import get_settings

router = APIRouter()


@router.get("/summary", response_model=BillingResponse)
def summary(
    user: User = Depends(current_user), db: Session = Depends(get_db)
) -> BillingResponse:
    return BillingResponse(**billing_summary(db, user))


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(user: User = Depends(current_user)) -> CheckoutResponse:
    settings = get_settings()
    checkout_url = settings.billing_checkout_url
    if not checkout_url:
        metrics.increment("billing.checkout_unconfigured")
        return CheckoutResponse(
            available=False,
            checkout_url=None,
            message="Billing provider is not configured. No payment has been attempted.",
        )
    metrics.increment("billing.checkout_requested")
    return CheckoutResponse(
        available=True,
        checkout_url=checkout_url,
        message="Continue to the configured billing provider to upgrade.",
    )
