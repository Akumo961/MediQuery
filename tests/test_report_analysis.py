import pytest

from src.services.report_analysis import (
    ReportValidationError,
    parse_findings,
)


def test_rejects_non_pdf_content() -> None:
    with pytest.raises(ReportValidationError, match="not a valid PDF"):
        from src.services.report_analysis import validate_pdf

        validate_pdf("report.pdf", "application/pdf", b"not-a-pdf", 1024)


def test_rejects_oversized_report() -> None:
    with pytest.raises(ReportValidationError, match="exceeds"):
        from src.services.report_analysis import validate_pdf

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


def test_parses_reference_and_flag_on_following_lines() -> None:
    text = """Hemoglobin: 11.2 g/dL
Reference Range: 12.0 - 16.0 g/dL
Flag: LOW
White Blood Cell Count: 7.4 x10^9/L
Reference Range: 4.0 - 11.0 x10^9/L
Flag: NORMAL
Platelets: 245 x10^9/L
Reference Range: 150 - 400 x10^9/L
Flag: NORMAL
Glucose: 126 mg/dL
Reference Range: 70 - 99 mg/dL
Flag: HIGH"""

    findings = parse_findings(text, page=1)

    assert len(findings) == 4
    assert [finding.name for finding in findings] == [
        "Hemoglobin",
        "White Blood Cell Count",
        "Platelets",
        "Glucose",
    ]
    assert [finding.value for finding in findings] == ["11.2", "7.4", "245", "126"]
    assert [finding.flag for finding in findings] == ["low", "normal", "normal", "high"]
    assert [finding.reference_range for finding in findings] == [
        "12.0 - 16.0 g/dL",
        "4.0 - 11.0 x10^9/L",
        "150 - 400 x10^9/L",
        "70 - 99 mg/dL",
    ]


def test_parses_numeric_multiplier_units_used_by_real_cbc_reports() -> None:
    text = """WBC: 11.8 10^3/uL (4.0-11.0) High
Platelets: 250 10^3/uL (150-400) Normal"""

    findings = parse_findings(text, page=3)

    assert [finding.name for finding in findings] == ["WBC", "Platelets"]
    assert [finding.unit for finding in findings] == ["10^3/uL", "10^3/uL"]
    assert [finding.value for finding in findings] == ["11.8", "250"]
    assert [finding.flag for finding in findings] == ["high", "normal"]


def test_does_not_consume_reference_range_as_numeric_unit() -> None:
    findings = parse_findings("Glucose: 5.4 (3.9-5.6) Normal", page=1)

    assert len(findings) == 1
    assert findings[0].unit is None
    assert findings[0].reference_range == "3.9-5.6"


def test_candidate_with_unsupported_format_is_counted_for_extraction_warning() -> None:
    from src.services.report_analysis import _parse_page_findings

    findings, partial_candidates = _parse_page_findings(
        "Vitamin D: 42 ???\nHemoglobin: 13.2 g/dL", page=1
    )

    assert len(findings) == 1
    assert partial_candidates == 1
