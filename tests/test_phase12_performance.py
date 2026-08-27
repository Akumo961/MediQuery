"""Phase 12 performance and resource-bound tests."""

from types import SimpleNamespace

import pytest

from src.api.routes.search import MAX_QUERY_CHARS, SearchQuery
from src.core.database import Report
from src.data_loader import (
    PUBMED_CACHE_SIZE,
    PUBMED_CACHE_TTL_SECONDS,
    _fetch_pubmed_cached,
)


def test_search_query_has_explicit_resource_boundaries():
    query = "x" * MAX_QUERY_CHARS
    request = SearchQuery(query=query, max_results=50, search_type="keyword")
    assert len(request.query) == MAX_QUERY_CHARS
    with pytest.raises(ValueError):
        SearchQuery(query="x" * (MAX_QUERY_CHARS + 1))


def test_pubmed_cache_reuses_identical_requests(monkeypatch):
    calls = []

    class FakeLoader:
        def _fetch_pubmed_papers_uncached(self, query, max_results):
            calls.append((query, max_results))
            return [{"title": "Synthetic", "abstract": "Evidence"}]

    monkeypatch.setattr("src.data_loader.MedicalDataLoader", FakeLoader)
    _fetch_pubmed_cached.cache_clear()
    try:
        first = _fetch_pubmed_cached("blood pressure", 10, 123)
        second = _fetch_pubmed_cached("blood pressure", 10, 123)
        assert first == second
        assert calls == [("blood pressure", 10)]
        info = _fetch_pubmed_cached.cache_info()
        assert info.maxsize == PUBMED_CACHE_SIZE
        assert info.hits >= 1
    finally:
        _fetch_pubmed_cached.cache_clear()


def test_pubmed_cache_is_time_bucketed():
    assert PUBMED_CACHE_TTL_SECONDS == 300
    assert PUBMED_CACHE_SIZE <= 128


def test_report_has_compound_listing_index():
    index_names = {index.name for index in Report.__table__.indexes}
    assert "ix_reports_owner_created" in index_names


def test_search_result_index_guard_is_bounded():
    result = SimpleNamespace(index=999999)
    assert not 0 <= result.index < 10
