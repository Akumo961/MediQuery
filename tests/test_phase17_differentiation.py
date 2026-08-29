from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_phase17_assets_exist_and_are_nonempty() -> None:
    required = [
        ROOT / "docs" / "DEMONSTRABLE_DIFFERENTIATION.md",
        ROOT / ".github" / "workflows" / "phase17-differentiation.yml",
        ROOT / "src" / "services" / "report_analysis.py",
        ROOT / "src" / "services" / "retrieval.py",
        ROOT / "src" / "api" / "routes" / "reports.py",
        ROOT / "src" / "core" / "billing.py",
        ROOT / "src" / "core" / "observability.py",
        ROOT / "src" / "api" / "main.py",
    ]
    for path in required:
        assert path.is_file(), path
        assert path.stat().st_size > 0, path


def test_phase17_documentation_declares_scope_and_boundaries() -> None:
    document = (
        ROOT / "docs" / "DEMONSTRABLE_DIFFERENTIATION.md"
    ).read_text(encoding="utf-8")
    assert "Phase 17" in document
    assert "What is deliberately not claimed" in document
    assert "Buyer demonstration script" in document
    assert "Phase 17 acceptance criteria" in document
