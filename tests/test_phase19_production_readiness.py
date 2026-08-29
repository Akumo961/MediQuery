from pathlib import Path

import pytest

from src.core.settings import Settings


ROOT = Path(__file__).resolve().parents[1]


def production_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "environment": "production",
        "database_url": "postgresql://mediquery:test@localhost/mediquery",
        "jwt_secret": "x" * 64,
        "cors_origins": ["https://app.example.test"],
        "metrics_token": "m" * 64,
    }
    values.update(overrides)
    return Settings(**values)


def test_production_rejects_development_jwt_secret() -> None:
    settings = production_settings(
        jwt_secret="development-only-change-me-before-production"
    )
    with pytest.raises(RuntimeError, match="JWT_SECRET"):
        settings.validate_for_runtime()


def test_production_rejects_short_jwt_secret() -> None:
    settings = production_settings(jwt_secret="too-short")
    with pytest.raises(RuntimeError, match="32 characters"):
        settings.validate_for_runtime()


def test_production_rejects_sqlite() -> None:
    settings = production_settings(database_url="sqlite:///./mediquery.db")
    with pytest.raises(RuntimeError, match="managed database"):
        settings.validate_for_runtime()


def test_production_rejects_http_cors() -> None:
    settings = production_settings(cors_origins=["http://app.example.test"])
    with pytest.raises(RuntimeError, match="HTTPS"):
        settings.validate_for_runtime()


def test_production_rejects_short_metrics_token() -> None:
    settings = production_settings(metrics_token="short")
    with pytest.raises(RuntimeError, match="METRICS_TOKEN"):
        settings.validate_for_runtime()


def test_phase19_document_contains_release_boundary() -> None:
    document = (
        (ROOT / "docs" / "PHASE19_PRODUCTION_READINESS.md")
        .read_text(encoding="utf-8")
        .lower()
    )
    for marker in (
        "phase 19",
        "production readiness",
        "acceptance criteria",
        "phi",
        "tls/waf",
        "backups",
        "malware scanning",
    ):
        assert marker in document, marker


def test_deployment_document_preserves_phihandoff_requirements() -> None:
    document = (ROOT / "DEPLOYMENT.md").read_text(encoding="utf-8").lower()
    for marker in (
        "managed postgres",
        "private encrypted object storage",
        "tls/waf",
        "secret manager",
        "backups/restore tests",
        "malware scanning",
    ):
        assert marker in document, marker


def test_local_database_and_env_are_ignored() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore
    assert "*.db" in gitignore
    assert "private_uploads/" in gitignore
