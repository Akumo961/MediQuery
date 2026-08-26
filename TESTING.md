# Testing

Run the local checks after installing `requirements.txt`:

```bash
python -m pytest -q
python -m compileall -q src app.py
```

The test suite uses synthetic data only. Coverage includes report MIME/signature/size validation, structured-value preservation, signup/consent, authentication and authorization, invalid PDF uploads, owner isolation, deletion, RAG provenance/injection boundaries, rate limiting, privacy-safe metrics, billing plan definitions, durable usage metering, idempotency, entitlement enforcement, authenticated billing summaries, honest unconfigured checkout behavior, and protection of the operational metrics endpoint.

Phase 9 billing tests deliberately do not pretend that payment processing is live. A real payment-provider adapter must be tested separately with provider sandbox credentials and webhook fixtures before charging customers.

Phase 10 observability tests verify that metrics are aggregate and that the metrics endpoint is not publicly readable without an explicitly configured collector token. Application logs intentionally record only request ID, method, route, status, and latency; they do not log report contents, filenames, tokens, or email addresses.

Before launch, add fixture-based tests for multi-page and malformed PDFs, upload resource limits, storage failures, migrations, RAG source attribution, prompt injection, urgent-language UX, keyboard/screen-reader flows, and browser-level sign-up/upload/delete journeys. Use synthetic reports only; do not commit patient data.

The repository CI workflow in `.github/workflows/ci.yml` is the authoritative repeatable quality gate for formatting, linting, tests, compilation, and credential-shaped secret scanning. Dependency/SBOM scanning and managed runtime monitoring should be enabled in the production environment.
