"""Buyer-facing end-to-end acceptance test for the primary MediQuery journey."""

import base64
from uuid import uuid4

from fastapi.testclient import TestClient

from src.api.main import app


SYNTHETIC_LAB_PDF = base64.b64decode(
    "JVBERi0xLjMKJZOMi54gUmVwb3J0TGFiIEdlbmVyYXRlZCBQREYgZG9jdW1lbnQgKG9wZW5zb3VyY2UpCjEgMCBvYmoKPDwKL0YxIDIgMCBSCj4+CmVuZG9iago="
    "MiAwIG9iago8PAovQmFzZUZvbnQgL0hlbHZldGljYSAvRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZyAvTmFtZSAvRjEgL1N1YnR5cGUgL1R5cGUxIC9UeXBlIC9Gb250Cj4+CmVuZG9iagozIDAgb2JqCjw8Ci9Db250ZW50cyA3IDAgUiAvTWVkaWFCb3ggWyAwIDAgNTk1LjI3NTYgODQxLjg4OTggXSAvUGFyZW50IDYgMCBSIC9SZXNvdXJjZXMgPDwKL0ZvbnQgMSAwIFIgL1Byb2NTZXQgWyAvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJIF0KPj4gL1JvdGF0ZSAwIC9UcmFucyA8PgoKPj4gCiAgL1R5cGUgL1BhZ2UKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1BhZ2VzIDYgMCBSIC9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9BdXRob3IgKGFub255bW91cykgL0NyZWF0aW9uRGF0ZSAoRDoyMDI2MDgzMDIwMzQxNyswMCcwMCcpIC9DcmVhdG9yIChhbm9ueW1vdXMpIC9LZXl3b3JkcyAoKSAvTW9kRGF0ZSAoRDoyMDI2MDgzMDIwMzQxNyswMCcwMCcpIC9Qcm9kdWNlciAoUmVwb3J0TGFiIFBERiBMaWJyYXJ5IC0gXChvcGVuc291cmNlXCkpIAogIC9TdWJqZWN0ICh1bnNwZWNpZmllZCkgL1RpdGxlICh1bnRpdGxlZCkgL1RyYXBwZWQgL0ZhbHNlCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9Db3VudCAxIC9LaWRzIFsgMyAwIFIgXSAvVHlwZSAvUGFnZXMKPj4KZW5kb2JqCjcgMCBvYmoKPDwKL0ZpbHRlciBbIC9BU0NJSTg1RGVjb2RlIC9GbGF0ZURlY29kZSBdIC9MZW5ndGggMjM3Cj4+CnN0cmVhbQpHYXNiUjlhY1A8J0xoY3FNUyNyNFNgYE0vOS1cRiImTWhdY1F1JjpPOzhNVyFWcUpwVTxda1ZiYSNXbSIhcGJTSTQiR2xEX2huXzFLQkZCL0ZNU1hXXEMnLXNOVllQXE8rRVhiYE5sUzFZMFROT0ovbSRtWjdhNj1yISduMT9vYGpeJShANlBqcjIwNU5xTjBWY3NXWSlRXTgoJU0sW0dIIyZtOmtBWTZlZkF1bW1YN1xrX0YmL1hVbU5WV2EnZCVaZS9bZUJkMXBXIU1XVSpZKTU5OixTaGlKXkZ0bF9ZQUIiTixIY0lmM2FSfj5lbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCA4CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDA2MSAwMDAwMCBuIAowMDAwMDAwMDkyIDAwMDAwIG4gCjAwMDAwMDAxOTkgMDAwMDAgbiAKMDAwMDAwMDQwMiAwMDAwMCBuIAowMDAwMDAwNDcwIDAwMDAwIG4gCjAwMDAwMDA3MzEgMDAwMDAgbiAKMDAwMDAwMDc5MCAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9JRCAKWzw1ZDExYzU2ODNlMTlhNWE0ZjZkM2U4YjM3ZjE2OThmYj48NWQxMWM1NjgzZTE5YTVhNGY2ZDNlOGIzN2YxNjk4ZmI+XQolIFJlcG9ydExhYiBnZW5lcmF0ZWQgUERGIGRvY3VtZW50IC0tIGRpZ2VzdCAob3BlbnNvdXJjZSkKCi9JbmZvIDUgMCBSCi9Sb290IDQgMCBSCi9TaXplIDgKPj4Kc3RhcnR4cmVmCjExMTcKJSVFT0YK"
)


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
            files={"file": ("synthetic-lab.pdf", SYNTHETIC_LAB_PDF, "application/pdf")},
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
