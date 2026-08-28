# MediQuery — Privacy-Conscious Medical Report Intelligence

> **Production-oriented AI engineering foundation for secure medical-report organization, structured extraction, and future grounded retrieval.**

**FastAPI** · **Python** · **PostgreSQL/SQLite** · **Streamlit** · **PDF Processing** · **FAISS** · **Docker** · **GitHub Actions** · **AI Safety**

## Overview

MediQuery is a privacy-conscious medical-report organization platform designed to help users securely upload text-based PDF reports, extract structured findings with source evidence, review the results, and manage their reports through an authenticated interface.

The project focuses on the engineering challenges around sensitive-document AI: **validation, authorization, tenant/owner isolation, conservative extraction, traceability, privacy-aware telemetry, testing, and safe AI integration boundaries**.

MediQuery is intentionally engineered so that experimental or planned AI capabilities are not presented as clinical functionality.

> **Medical safety boundary:** MediQuery is an educational report-organization tool. It is **not** a diagnostic service, emergency service, doctor replacement, or clinically validated medical device. Extracted information must be checked against the original report and discussed with a qualified healthcare professional.

## What is implemented

### Secure document workflow

- Authenticated signup/login and owner-scoped report access
- Server-side PDF validation using extension, MIME advisory checks, magic bytes, size, page count, encryption, and malformed-content checks
- Private generated storage keys instead of public report URLs
- Report history, detail, deletion, and account deletion
- Conservative structured extraction of values, units, reference ranges, explicit flags, page numbers, and source evidence
- Explicit handling of unsupported/scanned reports rather than fabricated extraction results

### AI engineering foundation

- Structured extraction pipeline with replaceable service boundaries
- Local FAISS retrieval utilities as an exploratory retrieval foundation
- Provider-agnostic architecture for future grounded AI capabilities
- Clear separation between deterministic extraction and future generative/RAG features
- Medical-AI safety boundary documented in `AI_SAFETY.md`

### Security, privacy & reliability

- JWT authentication and owner-scoped authorization
- Request IDs and PHI-conscious aggregate telemetry
- Rate-limit telemetry and safe error responses
- Security headers and explicit CORS configuration
- Environment-based secret management
- Production configuration that fails closed on insecure defaults
- Synthetic demonstration data for development/testing
- No production credentials or real patient data in the repository

### Testing & delivery

- Unit, API, security, extraction, authorization, deletion, telemetry, retrieval-contract, and entitlement tests
- Deterministic synthetic test data
- Formatting and linting checks
- Python compilation checks
- GitHub Actions quality gate
- Docker-based local deployment/smoke environment
- Documented production deployment requirements and operational gaps

## Architecture

```text
                         ┌──────────────────────┐
                         │   Streamlit Client   │
                         │ Upload / Review      │
                         └──────────┬───────────┘
                                    │ HTTPS + JWT
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │ Auth / API / Policy  │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐  ┌────────────────┐  ┌───────────────┐
        │ Upload         │  │ Structured     │  │ Entitlements  │
        │ Validation     │  │ Extraction     │  │ + Usage       │
        └───────┬────────┘  └───────┬────────┘  └───────────────┘
                │                   │
                ▼                   ▼
        ┌────────────────┐  ┌────────────────┐
        │ Private        │  │ PostgreSQL /   │
        │ Storage        │  │ SQLite         │
        └────────────────┘  └───────┬────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Owner-Scoped     │
                           │ Report Viewer    │
                           └──────────────────┘

                 Future / replaceable boundary
                           ┌───────────────┐
                           │ Curated RAG   │
                           │ + Grounded AI │
                           └───────────────┘
```

## AI / Retrieval Design

The protected report workflow deliberately keeps medical facts tied to source evidence instead of asking a free-form model to invent or reinterpret findings.

A future grounded AI workflow is designed around the following boundary:

```text
Medical Report
     │
     ▼
Validation / Extraction
     │
     ▼
Structured Findings + Page Evidence
     │
     ▼
Curated / Licensed Knowledge Base
     │
     ▼
Bounded Retrieval
     │
     ▼
Grounded Educational Explanation
     │
     ▼
Source Attribution + Safety Controls
```

Any generative medical feature must remain educational, source-attributed, bounded by retrieval, resistant to prompt injection, tenant-isolated, and evaluated before being considered for deployment.

## Engineering Principles

MediQuery is built around several principles:

1. **Security before AI** — authentication, authorization, validation, and privacy boundaries are application controls, not prompt instructions.
2. **Evidence over invention** — extracted values preserve page/source evidence and unsupported inputs produce explicit limitations.
3. **Replaceable AI boundaries** — vendor-specific models, storage, retrieval, and billing are isolated behind service interfaces.
4. **Fail closed** — insecure defaults and unsupported medical workflows should not silently become enabled production behavior.
5. **Measure before claiming** — accuracy, clinical usefulness, compliance, and production readiness are not claimed without reproducible evidence.

## Technology Stack

| Layer | Technologies |
|---|---|
| API | Python, FastAPI, Pydantic |
| Authentication | Password hashing, JWT, owner-scoped authorization |
| Data | SQLAlchemy, SQLite/PostgreSQL, Alembic |
| Documents | pypdf, server-side PDF validation, structured extraction |
| Retrieval | FAISS utilities / replaceable retrieval boundary |
| Client | Streamlit |
| Infrastructure | Docker, Docker Compose |
| Quality | Pytest, Black, Flake8, Compileall, GitHub Actions |
| Operations | Request IDs, rate-limit telemetry, PHI-conscious metrics |

## Repository Structure

```text
MediQuery/
├── src/
│   ├── api/                 # FastAPI application and routes
│   ├── models/              # Persistence models
│   ├── schemas/             # Pydantic contracts
│   ├── services/            # Extraction, retrieval, telemetry, billing, etc.
│   └── ...
├── tests/                   # Synthetic unit/API/security tests
├── app.py                   # Streamlit client
├── ARCHITECTURE.md          # System design and trust boundaries
├── SECURITY.md              # Security/privacy posture and gaps
├── AI_SAFETY.md             # Medical-AI safety boundary
├── TESTING.md               # Test strategy and release gaps
├── DEPLOYMENT.md            # Deployment requirements
├── PERFORMANCE.md           # Performance measurements and trade-offs
├── ACQUISITION.md           # Technical acquisition overview
└── BUYER_DUE_DILIGENCE.md   # Buyer risk assessment
```

## Quality Gate

Run locally:

```bash
python -m black --check src tests app.py
python -m flake8 src tests app.py --max-line-length=120
python -m pytest -q
python -m compileall -q src app.py
```

The GitHub Actions workflow provides the repeatable repository quality gate for formatting, linting, tests, compilation, and secret-shaped credential scanning.

## Local Development

### Prerequisites

- Python 3.11+
- Virtual environment
- Docker Desktop (optional for the production-shaped smoke environment)

### API

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn src.api.main:app --reload --port 8000
```

### Streamlit client

In a second terminal:

```bash
streamlit run app.py
```

The client defaults to `http://localhost:8000`. Set `MEDIQUERY_API_URL` when using another API endpoint.

### Development safety

**Use synthetic data only.** The local SQLite database and `private_uploads` directory are not suitable for real patient reports.

## Current Scope & Honest Limitations

MediQuery is a **production-shaped engineering foundation**, not a clinically validated product.

The following are intentionally **not currently implemented** in the protected report flow:

- Production generative-model integration
- Populated production medical RAG knowledge base
- Clinical diagnosis or clinical decision support
- OCR for scanned PDFs
- Live Stripe/payment processing
- Managed production storage/database/monitoring infrastructure
- Clinical validation or regulatory clearance
- Compliance certification such as HIPAA, PIPEDA, PHIPA, GDPR, or SOC 2
- Verified customer traction or revenue

Historical prototype artifacts or placeholder model/data files are not treated as evidence of a trained production model or validated accuracy.

## Production Deployment Requirements

A real sensitive-data deployment would require, at minimum:

1. Managed PostgreSQL with appropriate access controls.
2. Private encrypted object storage.
3. TLS behind an appropriate reverse proxy/WAF.
4. Managed secret storage and rotation.
5. Isolated asynchronous document processing.
6. Malware scanning and resource limits.
7. Backups and tested restore procedures.
8. PHI-conscious monitoring and error reporting.
9. Database migration and rollback procedures.
10. Legal, privacy, security, provider, and clinical review appropriate to the target market.

See `DEPLOYMENT.md` and `SECURITY.md` before considering sensitive-data deployment.

## Roadmap

### AI / Retrieval

- Evaluated synthetic extraction datasets
- OCR with measured extraction quality
- Curated, versioned, licence-reviewed medical knowledge retrieval
- Source-attributed educational explanations
- Retrieval and grounded-answer evaluation
- Human-factors and clinical review

### Production Engineering

- Managed Postgres and private object storage
- Isolated asynchronous workers
- Malware scanning
- Production monitoring
- Browser-level accessibility and responsive testing
- Stronger account recovery/session controls

### Commercialization

- Verified payment-provider webhooks
- Production web client if Streamlit no longer meets UX requirements
- Customer research and pricing validation
- Appropriate legal/privacy/security/regulatory work

## Licensing & IP

There is currently **no repository licence grant**. Do not assume the project is MIT-licensed or otherwise freely reusable.

Before commercial use, perform a dependency/model/data licence inventory and verify ownership, contributor rights, medical-source provenance, and third-party intellectual-property obligations.

## Disclaimer

MediQuery is an AI engineering and software-development project for educational and portfolio purposes. It does not provide medical diagnosis, treatment recommendations, emergency guidance, or clinical decision support.
