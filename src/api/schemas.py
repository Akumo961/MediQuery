"""Strict API contracts for accounts and structured report processing."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class SignUpRequest(BaseModel):
    email: str = Field(
        min_length=3, max_length=320, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    )
    password: str = Field(min_length=12, max_length=128)
    acknowledge_medical_limitations: bool = False


class LoginRequest(SignUpRequest):
    pass


class AuthResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class FindingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    value: str
    unit: str | None
    reference_range: str | None
    flag: Literal["high", "low", "normal", "unknown"]
    page: int
    evidence: str


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    original_filename: str
    status: str
    page_count: int
    extraction_note: str | None
    created_at: datetime
    findings: list[FindingResponse] = []


class PlanResponse(BaseModel):
    plan: Literal["free", "pro"]
    reports_used: int
    reports_limit: int | None
