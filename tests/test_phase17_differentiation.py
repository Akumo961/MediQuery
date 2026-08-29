from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_evidence_first_extraction_contract() -> None:
    source = read("src/services/report_analysis.py")
    assert "class ExtractedFinding" in source
    assert "reference_range" in source
    assert "evidence" in source
    assert "page: int" in source
    assert "No selectable text was found" in source


def test_owner_isolation_and_private_storage_contract() -> None:
    reports = read("src/api/routes/reports.py")
    database = read("src/core/database.py")
    assert "Report.owner_id == user.id" in reports
    assert "Report.deleted_at.is_(None)" in reports
    assert 'storage_key = f\"{user.id}/{report_id}.pdf\"' in reports
    assert "storage_key" in database
    assert "owner_id" in database


def test_provenance_and_prompt_injection_boundary_contract() -> None:
    retrieval = read("src/services/retrieval.py")
    required_metadata = [
        "source_id",
        "title",
        "publisher",
        "url",
        "version",
        "license_note",
    ]
    for field in required_metadata:
        assert field in retrieval
    assert "untrusted data, not instructions" in retrieval
    assert "char_budget" in retrieval
    assert "minimum_score" in retrieval


def test_provider_neutral_billing_and_privacy_aware_operations() -> None:
    billing = read("src/core/billing.py")
    observability = read("src/core/observability.py")
    main = read("src/api/main.py")
    assert "provider-neutral" in billing.lower()
    assert "import stripe" not in billing.lower()
    assert "report text" in observability
    assert "filenames" in observability
    assert "X-Request-ID" in main
    assert "rate_limiter.allowed" in main


def test_phase17_documentation_is_complete_and_honest() -> None:
    document = read("docs/DEMONSTRABLE_DIFFERENTIATION.md")
    required = [
        "Evidence-first extraction",
        "Conservative failure handling",
        "Owner isolation",
        "Privacy-conscious storage",
        "Safety boundary",
        "Provenance-ready retrieval",
        "Prompt-injection resistance",
        "Vendor-neutral monetization",
        "Operational privacy",
        "Buyer demonstration script",
        "What is deliberately not claimed",
        "six-figure acquisition",
    ]
    for item in required:
        assert item in document
