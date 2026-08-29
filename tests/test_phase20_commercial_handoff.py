from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


def test_phase20_package_contains_required_handoff_assets() -> None:
    required = (
        "docs/PHASE20_COMMERCIAL_HANDOFF.md",
        "RELEASE_CHECKLIST.md",
        "ACQUISITION.md",
        "BUYER_DUE_DILIGENCE.md",
        "docs/DEMONSTRABLE_DIFFERENTIATION.md",
        "docs/PHASE18_MEDICAL_AI_SAFETY.md",
        "docs/PHASE19_PRODUCTION_READINESS.md",
        "README.md",
        "SECURITY.md",
        "DEPLOYMENT.md",
    )
    for path in required:
        target = ROOT / path
        assert target.is_file() and target.stat().st_size > 0, path


def test_phase20_document_preserves_commercial_truthfulness() -> None:
    document = read("docs/PHASE20_COMMERCIAL_HANDOFF.md")
    for marker in (
        "phase 20",
        "commercial handoff",
        "acceptance criteria",
        "buyer handoff package",
        "external diligence",
        "synthetic reports only",
        "does not claim",
        "ip ownership",
        "customer demand",
    ):
        assert marker in document, marker


def test_phase20_does_not_turn_missing_external_evidence_into_claims() -> None:
    acquisition = read("ACQUISITION.md")
    due_diligence = read("BUYER_DUE_DILIGENCE.md")
    for document in (acquisition, due_diligence):
        assert "no verified customer traction" in document
        assert "no clinical validation" in document
        assert "legal" in document
        assert "ip" in document


def test_release_checklist_requires_all_phase_gates() -> None:
    checklist = read("RELEASE_CHECKLIST.md")
    for marker in (
        "phase 17 acceptance",
        "phase 18 acceptance",
        "phase 19 acceptance",
        "phase 20 acceptance",
        "exact release commit sha",
        "no local database",
        "credential-shaped secret",
    ):
        assert marker in checklist, marker


def test_repository_safety_boundaries_remain_explicit() -> None:
    readme = read("README.md")
    acquisition = read("ACQUISITION.md")
    security = read("SECURITY.md")
    deployment = read("DEPLOYMENT.md")
    combined = readme + acquisition + security + deployment
    assert "not a diagnostic service" in combined
    assert "not approved for real patient/phi processing" in combined
    assert "managed postgres" in deployment
    assert "tls/waf" in deployment
    assert "malware scanning" in deployment
