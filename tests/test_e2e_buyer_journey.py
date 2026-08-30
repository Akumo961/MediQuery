"""Buyer-facing end-to-end acceptance test for the primary MediQuery journey."""

from io import BytesIO
from uuid import uuid4

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from src.api.main import app


def _synthetic_lab_pdf() -> bytes:
    output = BytesIO()
    pdf = canvas.Canvas(output)
    lines = [
        "Hemoglobin: 13.2 g/dL",
        "WBC: 11.8 10^3/uL",
        "Reference Range: 4.0 - 11.0 10^3/uL",
        "Flag: High",
        "Platelets: 250 10^3/uL",
        "Reference Range: 150 - 400 10^3/uL",
        "Flag: Normal",
    ]
    for index, line in enumerate(lines):
        pdf.drawString(72, 750 - (index * 20), line)
    pdf.save()
    return output.getvalue()


def test_login_upload_extract_evidence_report_and_account_management() -> None:
    password = "a-long-enough-password"
    email = f"e2e-{uuid4().hex}@example.test"

    with TestClient(app) as client:
        signup = client.post(
            "/api/auth/signup",
            json={
                "email": email,
                "password": password,
                "acknowledge_medical_limitations": True,
            },
        )
        assert signup.status_code == 201

        login = client.post(
            "/api/auth/login", json={"email": email, "password": password}
        )
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        upload = client.post(
            "/api/reports",
            headers=headers,
            files={
                "file": (
                    "synthetic-lab.pdf",
                    _synthetic_lab_pdf(),
                    "application/pdf",
                )
            },
        )
        assert upload.status_code == 201
        report = upload.json()
        assert report["page_count"] == 1
        assert {finding["name"] for finding in report["findings"]} >= {
            "Hemoglobin",
            "WBC",
            "Platelets",
        }
        assert all(finding["page"] == 1 for finding in report["findings"])
        assert all(finding["evidence"] for finding in report["findings"])

        report_id = report["id"]
        listing = client.get("/api/reports", headers=headers)
        assert listing.status_code == 200
        assert any(item["id"] == report_id for item in listing.json())

        detail = client.get(f"/api/reports/{report_id}", headers=headers)
        assert detail.status_code == 200
        assert detail.json()["id"] == report_id

        deletion = client.delete("/api/auth/account", headers=headers)
        assert deletion.status_code == 204

        assert (
            client.post(
                "/api/auth/login", json={"email": email, "password": password}
            ).status_code
            == 401
        )
        assert client.get("/api/reports", headers=headers).status_code == 401
