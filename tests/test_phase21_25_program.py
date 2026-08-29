"""Acceptance tests for the final production-to-sale program."""

from pathlib import Path

import pytest

from src.core.compliance import CONTROLS, required_control_ids, validate_evidence_map
from src.core.production_readiness import ProductionRequirements, production_contract_is_complete
from src.frontend.accessibility import validate_interactive_metadata, validate_status_message
from src.services.evaluation import ExpectedFinding, evaluate_findings, retrieval_grounding_coverage
from src.services.release_manifest import ReleaseManifest, release_is_candidate

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


def test_phase21_document_and_production_contract_exist() -> None:
    document = read("docs/PHASE21_PRODUCTION_INFRASTRUCTURE.md")
    for marker in ("phase 21", "managed postgres", "tls/waf", "malware scanning", "backup", "fail closed"):
        assert marker in document
    requirements = ProductionRequirements(
        database_url="postgresql://managed",
        jwt_secret="x" * 32,
        cors_origins=("https://app.example",),
        object_storage=True,
        secret_manager=True,
        tls=True,
        waf=True,
        malware_scanning=True,
        backups_restore_tested=True,
        asynchronous_processing=True,
    )
    assert production_contract_is_complete(requirements)


def test_phase22_evaluation_is_deterministic() -> None:
    document = read("docs/PHASE22_AI_EVALUATION.md")
    for marker in ("phase 22", "synthetic benchmark", "precision", "recall", "provenance", "prompt injection"):
        assert marker in document
    result = evaluate_findings(
        [ExpectedFinding("Glucose", "5.2", "mmol/L"), ExpectedFinding("ignored", "x")],
        [ExpectedFinding("glucose", "5.2", "MMOL/L")],
    )
    assert result.matched == 1
    assert result.recall == 1.0
    assert retrieval_grounding_coverage(["a", "b"], ["a"]) == 0.5


def test_phase23_accessibility_contract_is_enforced() -> None:
    document = read("docs/PHASE23_COMMERCIAL_PRODUCT.md")
    for marker in ("phase 23", "accessibility", "keyboard", "responsive", "accessible name"):
        assert marker in document
    validate_interactive_metadata({"label": "Upload", "name": "upload", "description": "Choose a PDF"})
    validate_status_message("Upload complete", "status")
    with pytest.raises(ValueError):
        validate_interactive_metadata({"label": "", "name": "upload", "description": "Choose a PDF"})


def test_phase24_compliance_readiness_is_evidence_based() -> None:
    document = read("docs/PHASE24_TRUST_SECURITY_COMPLIANCE.md")
    for marker in ("phase 24", "threat model", "privacy", "clinical review", "ip", "not a certification"):
        assert marker in document
    assert len(required_control_ids()) == len(CONTROLS)
    evidence = {control.control_id: "external-review-record" for control in CONTROLS}
    validate_evidence_map(evidence)


def test_phase25_release_manifest_fails_closed() -> None:
    document = read("docs/PHASE25_FINAL_SALE_READINESS.md")
    for marker in ("phase 25", "buyer data room", "release manifest", "exact commit", "external diligence"):
        assert marker in document
    manifest = ReleaseManifest(
        commit="abcdef1234567",
        tests="pass",
        quality="pass",
        phase_gates=("17", "18", "19", "20", "21", "22", "23", "24"),
        medical_safety_boundary="MediQuery is not a diagnostic service.",
    )
    assert release_is_candidate(manifest)
    assert not release_is_candidate(
        ReleaseManifest(
            commit="abc",
            tests="pass",
            quality="pass",
            phase_gates=manifest.phase_gates,
            medical_safety_boundary=manifest.medical_safety_boundary,
        )
    )
