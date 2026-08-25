# Testing

Run the local checks after installing `requirements.txt`:

```bash
python -m pytest -q
python -m compileall -q src app.py
```

The included tests use only synthetic strings and invalid files. They cover report MIME/signature/size validation, structured-value preservation, signup/consent, authorization required for report routes, rejection of an invalid PDF upload, owner isolation, deletion, RAG provenance/injection boundaries, and rate-limit/metric primitives.

Before launch, add fixture-based tests for multi-page and malformed PDFs, upload resource limits, owner isolation, deletion/account deletion, password reset, rate limiting, storage failures, migrations, RAG source attribution, prompt injection, urgent-language UX, keyboard/screen-reader flows, and browser-level sign-up/upload/delete journeys. Use synthetic reports only; do not commit patient data.

The current run produced `6 passed` on 2026-08-25. This is a foundation, not comprehensive clinical or production validation.

GitHub Actions in `.github/workflows/ci.yml` repeats formatting, linting, tests, compilation, and a credential-shape scan for pushes and pull requests. Dependency/SBOM scanning should be added through the chosen repository/security platform before launch.
