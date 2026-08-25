# MediQuery

MediQuery is an early-stage, privacy-conscious medical-report organization product. It accepts authenticated uploads of text-based PDF reports and surfaces conservative, structured extraction candidates—values, units, reference ranges, explicit flags, source page, and evidence—to help users review a report with a qualified clinician.

It is not a diagnostic tool, emergency service, doctor replacement, or clinically validated medical device. It does not claim HIPAA, PIPEDA, PHIPA, GDPR, SOC 2, or other compliance certification.

## What is implemented

- FastAPI service with account signup/login and owner-scoped reports.
- PDF validation, page limits, generated private storage keys, report/account deletion, and safe errors.
- Deterministic structured extraction candidates with page-level evidence.
- A simple responsive Streamlit client for sign-up, upload, review, and deletion.
- Landing/onboarding content with limitations acknowledgement, privacy messaging, plan boundary, and FAQ.
- A Free/Pro entitlement boundary (Free limit is configurable; billing is not enabled).
- Baseline security headers, CORS allowlist, environment validation, test coverage, container build, and operations documentation.

The legacy literature-search utilities remain exploratory. Gemini, Pinecone, real image-analysis models, a production React/Next.js app, RAG-based medical explanation, OCR, billing, and production monitoring are not implemented as product features in this repository.

## Architecture

The product follows a small API → validated extraction → private storage/database → owner-scoped viewer path. See [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY.md](SECURITY.md), and [AI_SAFETY.md](AI_SAFETY.md) for boundaries and remaining work.

## Local development

Prerequisites: Python 3.11+ and a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn src.api.main:app --reload --port 8000
```

In a second terminal:

```bash
streamlit run app.py
```

Use synthetic files only in local development. The default SQLite database and local `private_uploads` directory are not suitable for real medical data.

## Environment

Start from `.env.example`. `JWT_SECRET`, database credentials, AI/provider tokens, storage credentials, and other sensitive configuration must remain server-side and be provided by a secret manager in production. Production fails closed for a default/short JWT secret, SQLite, and HTTP CORS origins.

## Testing

```bash
python -m pytest -q
python -m compileall -q src app.py
```

See [TESTING.md](TESTING.md) for scope and gaps. No real patient data belongs in fixtures, screenshots, logs, or commits.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md). `docker compose up --build` is a local production-shaped smoke environment; it intentionally requires injected secrets and a managed database URL. It is not a complete production deployment.

## Roadmap

1. Managed private storage/Postgres, migrations, worker isolation, malware scanning, backups, and monitoring.
2. OCR and evaluated report extraction across synthetic layouts.
3. Source-attributed, curated RAG with adversarial safety evaluation.
4. Password reset/verification, billing provider, accessible production web client, and user research.
5. Legal, privacy, security, clinical, and accessibility reviews before processing real reports.

## Licence and contact

No licence is currently granted because a third-party dependency/model/data and ownership review is still required. Do not assume the repository is MIT-licensed merely because older documentation said so. See [ACQUISITION.md](ACQUISITION.md) and [BUYER_DUE_DILIGENCE.md](BUYER_DUE_DILIGENCE.md) for an honest technical diligence view.
