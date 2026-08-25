"""Authenticated, owner-scoped report lifecycle endpoints."""

from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from src.api.dependencies import current_user
from src.api.schemas import PlanResponse, ReportResponse
from src.core.database import AuditEvent, Report, ReportFinding, User, get_db
from src.core.settings import get_settings
from src.core.observability import metrics
from src.services.report_analysis import (
    ReportValidationError,
    extract_report,
    validate_pdf,
)

router = APIRouter()


def _get_owned_report(report_id: str, user: User, db: Session) -> Report:
    report = db.scalar(
        select(Report)
        .where(
            Report.id == report_id,
            Report.owner_id == user.id,
            Report.deleted_at.is_(None),
        )
        .options(selectinload(Report.findings))
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def upload_report(
    file: UploadFile = File(...),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> Report:
    settings = get_settings()
    count = (
        db.scalar(
            select(func.count())
            .select_from(Report)
            .where(Report.owner_id == user.id, Report.deleted_at.is_(None))
        )
        or 0
    )
    if user.plan == "free" and count >= settings.free_report_limit:
        raise HTTPException(status_code=402, detail="Free plan report limit reached")
    raw = await file.read(settings.max_report_bytes + 1)
    try:
        validate_pdf(file.filename, file.content_type, raw, settings.max_report_bytes)
        extraction = extract_report(raw, settings.max_pdf_pages)
    except ReportValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        await file.close()

    report_id = str(uuid4())
    storage_key = f"{user.id}/{report_id}.pdf"
    target = settings.upload_root / storage_key
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    report = Report(
        id=report_id,
        owner_id=user.id,
        original_filename=Path(file.filename or "report.pdf").name,
        storage_key=storage_key,
        page_count=extraction.page_count,
        extraction_note=extraction.note,
    )
    db.add(report)
    db.flush()
    for finding in extraction.findings:
        db.add(ReportFinding(report_id=report.id, **finding.__dict__))
    db.add(
        AuditEvent(
            actor_id=user.id,
            action="report_uploaded",
            target_id=report.id,
            metadata_json={
                "pages": extraction.page_count,
                "finding_count": len(extraction.findings),
            },
        )
    )
    db.commit()
    db.refresh(report)
    metrics.increment("reports.processed")
    if extraction.note:
        metrics.increment("reports.extraction_attention_required")
    return _get_owned_report(report.id, user, db)


@router.get("", response_model=list[ReportResponse])
def list_reports(
    user: User = Depends(current_user), db: Session = Depends(get_db)
) -> list[Report]:
    return list(
        db.scalars(
            select(Report)
            .where(Report.owner_id == user.id, Report.deleted_at.is_(None))
            .options(selectinload(Report.findings))
            .order_by(Report.created_at.desc())
        )
    )


@router.get("/plan", response_model=PlanResponse)
def get_plan(
    user: User = Depends(current_user), db: Session = Depends(get_db)
) -> PlanResponse:
    settings = get_settings()
    used = (
        db.scalar(
            select(func.count())
            .select_from(Report)
            .where(Report.owner_id == user.id, Report.deleted_at.is_(None))
        )
        or 0
    )
    return PlanResponse(
        plan=user.plan,
        reports_used=used,
        reports_limit=None if user.plan == "pro" else settings.free_report_limit,
    )


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)
) -> Report:
    return _get_owned_report(report_id, user, db)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)
) -> None:
    report = _get_owned_report(report_id, user, db)
    settings = get_settings()
    target = settings.upload_root / report.storage_key
    if target.exists():
        target.unlink()
    db.delete(report)
    db.add(
        AuditEvent(
            actor_id=user.id,
            action="report_deleted",
            target_id=report_id,
            metadata_json={},
        )
    )
    db.commit()
    metrics.increment("reports.deleted")
