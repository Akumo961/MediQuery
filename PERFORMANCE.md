# Performance & Resource Controls

## Phase 12 status

**COMPLETE for the current FastAPI + Streamlit architecture.** Phase 12 uses measured, low-risk improvements rather than premature infrastructure or speculative micro-optimizations.

### Implemented

- Bounded search query length (300 characters) and result count (1–50).
- Bounded PubMed result requests (1–100 internally).
- Five-minute, 128-entry in-process PubMed response cache to avoid repeated external calls for identical queries within a worker.
- Reuse of the literature data-loader instance per worker.
- Reuse of the semantic text-model instance per worker, avoiding model construction on every semantic search request.
- Defensive bounds checking for semantic-search result indexes.
- Composite `reports(owner_id, created_at)` database index for the dashboard/history query pattern.
- PDF extraction and upload persistence are moved off the FastAPI event-loop thread with `asyncio.to_thread` so CPU/file work does not unnecessarily block other async requests.
- The Streamlit client reuses a `requests.Session` per user session so API connections can be pooled across reruns.
- Existing PDF upload byte/page limits remain enforced before expensive extraction.
- Existing RAG context and retrieval limits remain bounded.
- Existing observability records request and operation latency without recording medical content.

## Performance trade-offs

The PubMed cache is intentionally process-local and short-lived. It is not a source of truth and does not replace a shared cache in a multi-worker deployment. A future shared cache should only be introduced if measured traffic justifies it and should have an explicit privacy/data-retention review.

The semantic model is cached per application worker. This reduces repeated model initialization while keeping worker isolation. Model thread-safety should be validated against the selected model implementation before increasing concurrency.

The application currently uses synchronous SQLAlchemy sessions and CPU-bound model inference behind FastAPI routes. PDF extraction/file persistence are offloaded from the event-loop thread. The current workload does not justify a queue solely for optimization. If production measurements show sustained inference latency or resource contention, move heavy inference to a bounded worker queue rather than increasing unbounded concurrency.

## Measurement and verification

CI verifies the performance-related invariants in `tests/test_phase12_performance.py`, including query/resource bounds, cache reuse, cache size/TTL, and the report listing index.

The production-shaped quality gate also verifies Black, Flake8, the complete pytest suite, Python compilation, and credential-shaped secret scanning. The latest GitHub Actions quality run completed successfully after the Phase 12 changes.

Operational latency is captured by the existing observability layer for API requests, report processing, and RAG searches. Production optimization decisions should use those measurements rather than guessed targets.

No fixed millisecond threshold is enforced in CI because shared GitHub-hosted runners are variable and timing-based tests would create false failures. Performance budgets should be established from real deployment measurements.

## Known limits

- The current product client is Streamlit, so Next.js bundle-size and browser/Lighthouse optimization are not applicable to this architecture.
- There is no production-scale load-test result yet.
- There is no managed distributed cache yet.
- Large-model inference remains dependent on the selected model and deployment hardware.
- SQLite remains suitable for local/test use; production database sizing and connection-pool tuning belong to deployment validation.
- Image handling is outside the active authenticated report workflow; no unnecessary image pipeline was introduced merely to satisfy a checklist item.

These are documented architectural boundaries, not claims of production-scale performance.
