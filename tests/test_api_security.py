from fastapi.testclient import TestClient
from io import BytesIO
from uuid import uuid4
from pypdf import PdfWriter

from src.api.main import app


def test_account_endpoints_require_unique_credentials() -> None:
    with TestClient(app) as client:
        email = f"person-{uuid4().hex}@example.test"
        response = client.post(
            "/api/auth/signup",
            json={
                "email": email,
                "password": "a-long-enough-password",
                "acknowledge_medical_limitations": True,
            },
        )
        assert response.status_code == 201
        assert response.json()["token_type"] == "bearer"
        duplicate = client.post(
            "/api/auth/signup",
            json={
                "email": email,
                "password": "a-long-enough-password",
                "acknowledge_medical_limitations": True,
            },
        )
        assert duplicate.status_code == 409


def test_signup_requires_medical_limitations_acknowledgement() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/auth/signup",
            json={
                "email": f"unacknowledged-{uuid4().hex}@example.test",
                "password": "a-long-enough-password",
            },
        )
        assert response.status_code == 422


def test_report_routes_require_authentication() -> None:
    with TestClient(app) as client:
        response = client.get("/api/reports")
        assert response.status_code == 401


def test_upload_rejects_invalid_pdf_for_authenticated_user() -> None:
    with TestClient(app) as client:
        token = client.post(
            "/api/auth/signup",
            json={
                "email": f"uploader-{uuid4().hex}@example.test",
                "password": "a-long-enough-password",
                "acknowledge_medical_limitations": True,
            },
        ).json()["access_token"]
        response = client.post(
            "/api/reports",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("not-a-report.pdf", b"not a pdf", "application/pdf")},
        )
        assert response.status_code == 422


def test_report_is_private_and_deletable() -> None:
    output = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(output)
    with TestClient(app) as client:
        password = "a-long-enough-password"
        owner = client.post(
            "/api/auth/signup",
            json={
                "email": f"owner-{uuid4().hex}@example.test",
                "password": password,
                "acknowledge_medical_limitations": True,
            },
        ).json()["access_token"]
        other = client.post(
            "/api/auth/signup",
            json={
                "email": f"other-{uuid4().hex}@example.test",
                "password": password,
                "acknowledge_medical_limitations": True,
            },
        ).json()["access_token"]
        created = client.post(
            "/api/reports",
            headers={"Authorization": f"Bearer {owner}"},
            files={"file": ("synthetic.pdf", output.getvalue(), "application/pdf")},
        )
        assert created.status_code == 201
        report_id = created.json()["id"]
        assert (
            client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": f"Bearer {other}"},
            ).status_code
            == 404
        )
        assert (
            client.delete(
                f"/api/reports/{report_id}",
                headers={"Authorization": f"Bearer {owner}"},
            ).status_code
            == 204
        )
