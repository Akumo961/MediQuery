"""Failure-path tests for external AI/literature dependencies."""

from fastapi.testclient import TestClient

from src.api.main import app
from src.api.routes import search


def test_literature_provider_failure_returns_safe_error(monkeypatch) -> None:
    class BrokenLoader:
        def fetch_pubmed_papers(self, *_args, **_kwargs):
            raise RuntimeError("synthetic upstream failure")

    monkeypatch.setattr(search, "MedicalDataLoader", BrokenLoader)
    with TestClient(app) as client:
        response = client.post(
            "/api/search/literature",
            json={"query": "synthetic anemia", "max_results": 5, "search_type": "keyword"},
        )
    assert response.status_code == 502
    assert response.json()["detail"] == "Literature search is temporarily unavailable"
    assert "synthetic upstream failure" not in response.text
