from io import BytesIO
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from src.api.main import app
from src.services.report_analysis import ReportValidationError, extract_report


def synthetic_pdf(page_count: int = 1, encrypted: bool = False) -> bytes:
    output = BytesIO()
    writer = PdfWriter()
    for _ in range(page_count):
        writer.add_blank_page(width=72, height=72)
    if encrypted:
        writer.encrypt("synthetic-test-password")
    writer.write(output)
    return output.getvalue()


def signup(client: TestClient, prefix: str) -> str:
    response = client.post(
        "/api/auth/signup",
        json={
            "email": f"{prefix}-{uuid4().hex}@example.test",
            "password": "a-long-enough-password",
            "acknowledge_medical_limitations": True,
        },
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def test_multi_page_synthetic_report_preserves_page_count() -> None:
    result = extract_report(synthetic_pdf(page_count=3), max_pages=5)
    assert result.page_count == 3
    assert result.findings == []
    assert result.note is not None


def test_synthetic_report_page_limit_is_enforced() -> None:
    with pytest.raises(ReportValidationError, match="too many pages"):
        extract_report(synthetic_pdf(page_count=3), max_pages=2)


def test_encrypted_synthetic_report_is_rejected() -> None:
    with pytest.raises(ReportValidationError, match="Password-protected PDFs"):
        extract_report(synthetic_pdf(encrypted=True), max_pages=5)


def test_login_returns_a_fresh_bearer_token() -> None:
    with TestClient(app) as client:
        email = f"login-{uuid4().hex}@example.test"
        password = "a-long-enough-password"
        created = client.post(
            "/api/auth/signup",
            json={
                "email": email,
                "password": password,
                "acknowledge_medical_limitations": True,
            },
        )
        assert created.status_code == 201
        login = client.post(
            "/api/auth/login", json={"email": email, "password": password}
        )
        assert login.status_code == 200
        assert login.json()["token_type"] == "bearer"
        assert login.json()["access_token"]


def test_wrong_password_is_rejected_without_account_enumeration() -> None:
    with TestClient(app) as client:
        email = f"wrong-password-{uuid4().hex}@example.test"
        password = "a-long-enough-password"
        client.post(
            "/api/auth/signup",
            json={
                "email": email,
                "password": password,
                "acknowledge_medical_limitations": True,
            },
        )
        response = client.post(
            "/api/auth/login",
            json={"email": email, "password": "definitely-wrong-password"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"


def test_end_to_end_upload_history_delete_journey() -> None:
    with TestClient(app) as client:
        token = signup(client, "e2e")
        headers = {"Authorization": f"Bearer {token}"}
        created = client.post(
            "/api/reports",
            headers=headers,
            files={
                "file": (
                    "synthetic-multi-page.pdf",
                    synthetic_pdf(page_count=2),
                    "application/pdf",
                )
            },
        )
        assert created.status_code == 201
        report = created.json()
        assert report["page_count"] == 2

        history = client.get("/api/reports", headers=headers)
        assert history.status_code == 200
        assert any(item["id"] == report["id"] for item in history.json())

        detail = client.get(f"/api/reports/{report['id']}", headers=headers)
        assert detail.status_code == 200
        assert detail.json()["id"] == report["id"]

        deleted = client.delete(f"/api/reports/{report['id']}", headers=headers)
        assert deleted.status_code == 204
        assert (
            client.get(f"/api/reports/{report['id']}", headers=headers).status_code
            == 404
        )


def test_account_deletion_revokes_access_to_owned_reports() -> None:
    with TestClient(app) as client:
        token = signup(client, "account-delete")
        headers = {"Authorization": f"Bearer {token}"}
        created = client.post(
            "/api/reports",
            headers=headers,
            files={
                "file": (
                    "synthetic.pdf",
                    synthetic_pdf(),
                    "application/pdf",
                )
            },
        )
        assert created.status_code == 201
        report_id = created.json()["id"]

        deleted = client.delete("/api/auth/account", headers=headers)
        assert deleted.status_code == 204
        assert (
            client.get(f"/api/reports/{report_id}", headers=headers).status_code == 401
        )


def test_unsupported_upload_format_has_a_safe_error() -> None:
    with TestClient(app) as client:
        token = signup(client, "unsupported")
        response = client.post(
            "/api/reports",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("report.txt", b"synthetic medical data", "text/plain")},
        )
        assert response.status_code == 422
        assert "PDF" in response.json()["detail"]
