# Testing

MediQuery uses synthetic data only. No real patient data belongs in the repository, fixtures, logs, CI artifacts, or bug reports.

## Local quality gate

After installing `requirements.txt`:

```bash
python -m black --check src tests app.py
python -m flake8 src tests app.py
python -m pytest -q
python -m compileall -q src app.py
```

The repository CI workflow in `.github/workflows/ci.yml` is the authoritative repeatable quality gate for formatting, linting, tests, compilation, and credential-shaped secret scanning.

## Test coverage

The suite covers:

- PDF MIME, extension, signature, size, malformed-content, and page-count validation
- Multi-page synthetic PDF handling
- Password-protected/encrypted PDF rejection
- Structured-value preservation including units, ranges, flags, page numbers, and evidence
- Synthetic report extraction failure/attention states
- Signup and medical-limitations acknowledgement
- Duplicate-account protection
- Login success and invalid-credential handling
- Authentication and authorization boundaries
- Owner isolation for reports
- End-to-end authenticated upload → history → detail → delete flow
- Account deletion and access revocation
- Unsupported upload-format handling
- Report deletion
- Rate limiting
- Privacy-safe aggregate metrics
- RAG provenance, relevance selection, citations, bounded context, and prompt-injection framing
- Billing plan definitions, durable usage metering, idempotency, entitlement enforcement, authenticated billing summaries, honest unconfigured checkout behavior, and protected operational metrics

## Synthetic fixtures

`tests/test_phase11_quality.py` generates PDFs in memory with `pypdf`. Fixtures are intentionally synthetic and contain no patient identifiers or clinical records.

## Provider-bound testing

Some functionality cannot be truthfully tested as a live external service inside the unit/API suite:

- Stripe/payment-provider sandbox and webhook delivery
- Production object storage and backup deletion
- Managed telemetry/error-reporting delivery
- OCR provider behavior
- Production database migration/rollback against the deployed database engine

Those require provider-specific sandbox credentials and deployment fixtures. The application must not simulate successful payment, clinical validation, or provider delivery merely to make tests pass.

## Remaining release-level tests

Before a real customer launch, add browser-level Playwright/Cypress coverage for responsive layout, keyboard navigation, screen-reader semantics, sign-up/upload/review/delete journeys, and urgent-language UX. Run those against the deployed staging environment. Also enable dependency/SBOM scanning and managed runtime monitoring in production.
