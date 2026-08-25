import pytest

from src.services.report_analysis import (
    ReportValidationError,
    parse_findings,
    validate_pdf,
)


def test_rejects_non_pdf_content() -> None:
    with pytest.raises(ReportValidationError, match="not a valid PDF"):
        validate_pdf("report.pdf", "application/pdf", b"not-a-pdf", 1024)


def test_rejects_oversized_report() -> None:
    with pytest.raises(ReportValidationError, match="exceeds"):
        validate_pdf("report.pdf", "application/pdf", b"%PDF-" + b"x" * 100, 32)


def test_preserves_value_unit_range_flag_and_evidence() -> None:
    findings = parse_findings("Hemoglobin: 9.8 g/dL (12.0-16.0) Low", page=2)
    assert len(findings) == 1
    finding = findings[0]
    assert finding.value == "9.8"
    assert finding.unit == "g/dL"
    assert finding.reference_range == "12.0-16.0"
    assert finding.flag == "low"
    assert finding.page == 2
    assert "Hemoglobin" in finding.evidence
