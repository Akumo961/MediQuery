# Performance & Resource Controls

## Phase 12 status

Phase 12 is focused on measured, low-risk improvements rather than premature infrastructure or speculative micro-optimizations.

### Implemented

- Bounded search query length (300 characters) and result count (1–50).
- Bounded PubMed result requests (1–100 internally).
- Five-minute, 128-entry in-process PubMed response cache to avoid repeated external calls for identical queries within a worker.
- Reuse of the literature data-loader instance per worker.
- Reuse of the semantic text-model instance per worker, avoiding model construction on every semantic search request.
- Defensive bounds checking for semantic-search result indexes.
- Composite `reports(owner_id, created_at)` database index for the dashboard/history query pattern.
- Existing PDF upload byte/page limits remain enforced before expensive extraction.
- Existing RAG context and retrieval limits remain bounded.
- Existing observability records request and operation latency without recording medical content.

## Performance trade-offs

The PubMed cache is intentionally process-local and short-lived. It is not a source of truth and does not replace a shared cache in a multi-worker deployment. A future shared cache should only be introduced if measured traffic justifies it and should have an explicit privacy/data-retention review.

The semantic model is cached per application worker. This reduces repeated model initialization while keeping worker isolation. Model thread-safety should be validated against the selected model implementation before increasing concurrency.

The application currently uses synchronous SQLAlchemy sessions and CPU-bound PDF/model operations behind FastAPI routes. The current workload does not justify a queue solely for optimization. If production measurements show event-loop blocking or sustained processing latency, move heavy extraction/inference to a bounded worker queue rather than increasing unbounded concurrency.

## Measurement and verification

CI verifies the performance-related invariants in `tests/test_phase12_performance.py`, including query/resource bounds, cache reuse, cache size/TTL, and the report listing index.

Operational latency is captured by the existing observability layer for API requests, report processing, and RAG searches. Production optimization decisions should use those measurements rather than guessed targets.

No fixed millisecond threshold is enforced in CI because shared GitHub-hosted runners are variable and timing-based tests would create false failures. Performance budgets should be established from real deployment measurements.

## Known limits

- There is no browser/Lighthouse baseline because the current product client is not a Next.js application.
- There is no production-scale load-test result yet.
- There is no managed distributed cache yet.
- Large-model inference remains dependent on the selected model and deployment hardware.
- SQLite remains suitable for local/test use; production database sizing and connection-pool tuning belong to deployment validation.

These are documented limitations, not claims of production-scale performance.
