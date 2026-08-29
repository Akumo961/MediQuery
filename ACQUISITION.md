# MediQuery — Acquisition Package

## 1. Executive summary

MediQuery is a lean medical-report organization platform built around authenticated report upload, conservative structured extraction, evidence preservation, owner-scoped access, usage entitlements, and privacy-conscious operational controls.

The acquisition value is **not** a claim of clinical capability, regulatory approval, revenue, or market traction. The current asset is an engineering foundation that reduces the work required to turn a prototype into a validated commercial workflow.

**Current status:** production-shaped engineering foundation; **not approved for real patient/PHI processing**.

## 2. Implemented vs. potential

### Implemented

- FastAPI API with authentication and authorization.
- Owner-scoped report history/detail/deletion.
- Server-side PDF validation and conservative structured extraction.
- Preservation of values, units, reference ranges, explicit flags, page numbers, and source evidence.
- Account deletion and report deletion paths.
- Server-side Free/Pro entitlement abstraction and durable usage metering.
- Request IDs, aggregate operational telemetry, rate-limit counters, and protected metrics.
- Containerized local deployment path.
- Automated formatting, linting, tests, compilation, and credential-pattern scanning.
- Documentation covering architecture, security, AI safety, testing, deployment, performance, acquisition, and buyer due diligence.

### Potential / not currently represented as implemented product capability

- Production Gemini or other generative-model integration.
- Populated, curated medical RAG knowledge base/Pinecone deployment.
- OCR for scanned reports.
- Clinical interpretation, diagnosis, triage, or clinical decision support.
- Live Stripe billing and webhook reconciliation.
- Managed cloud database/object storage/observability.
- Production Next.js/React web application.
- Clinical validation, regulatory clearance, compliance certification, customer traction, or revenue.

This separation is intentional and should be preserved during diligence.

## 3. Technical assets

A buyer receives a working source repository containing:

- API and persistence layer.
- Authentication/authorization boundaries.
- Document validation and extraction pipeline.
- Structured report/finding schemas.
- Retrieval foundation with provenance contracts.
- Entitlement and usage-metering foundation.
- Operational telemetry foundation.
- Streamlit application client.
- Automated tests and synthetic report fixtures.
- Docker/Compose deployment artifacts.
- Engineering and operational documentation.

## 4. Architecture

The architecture is intentionally small: client → authenticated API → validation/extraction → private storage/database → owner-scoped report viewer. Vendor-specific AI, retrieval, billing, storage, and telemetry capabilities are designed as replaceable boundaries.

This limits infrastructure cost and gives a future engineering team a clear migration path toward managed services without requiring a platform rewrite.

See `ARCHITECTURE.md` for trust boundaries and deployment details.

## 5. AI capabilities and safety posture

The protected report workflow deliberately does not convert unverified generative output into medical facts. The extraction representation retains source evidence and explicitly handles unreadable/scanned reports as limitations.

The retrieval code provides provenance, relevance filtering, bounded context, and prompt-injection framing, but it is **not** a populated production medical knowledge base.

Any future medical-information explanation capability should be introduced only after source licensing, evaluation, clinical/human-factors review, prompt-injection testing, citation verification, and operational controls are established.

## 6. RAG infrastructure

The repository contains a reusable retrieval foundation with mandatory source metadata and attribution contracts. It can support a curated knowledge workflow, but a buyer must not interpret its presence as evidence of production medical RAG quality or clinical accuracy.

The architecture is suitable for adding Pinecone or another managed vector service if evaluation demonstrates that the additional infrastructure is justified.

## 7. User experience

The current client supports a straightforward authenticated journey:

1. Create an account and acknowledge the product limitations.
2. Upload a supported text-based PDF.
3. Process the report through server-side validation/extraction.
4. Review extracted candidates with evidence and page references.
5. Delete the report when it is no longer required.

A production-grade web experience remains a product investment rather than something this repository should falsely represent as complete.

## 8. Deployment and operations

The repository includes a production-shaped local container environment and deployment guidance. Production use requires managed Postgres, private encrypted object storage, TLS/WAF, secret management, isolated asynchronous processing, malware scanning, backups/restore testing, monitoring, migrations, and appropriate provider/legal agreements.

The current repository does not provide evidence of a live production SLA, uptime history, disaster-recovery exercise, or managed observability account.

## 9. Security controls

Implemented controls include authentication, owner-scoped access, upload validation, private generated storage keys, deletion paths, security headers, CORS restrictions, safe errors, request IDs, rate limiting, and privacy-conscious telemetry.

These controls do **not** establish HIPAA, PIPEDA, PHIPA, GDPR, SOC 2, or any other compliance certification. Security suitability for real medical data depends on deployment configuration, contracts, policies, operations, and independent review.

## 10. Potential customers

Potential customer categories, subject to validation, include:

- Consumer health-navigation products.
- Clinics and allied-health organizations needing patient-facing report organization.
- Laboratories or benefits/navigation providers seeking a report-review workflow component.
- Health-tech platforms seeking a white-label report-ingestion and organization layer.

These are **potential markets**, not existing customers.

## 11. Potential acquirers

Potential acquirer categories, subject to strategic fit and diligence, include:

- Digital-health companies.
- Health-navigation and benefits platforms.
- Laboratory/diagnostic software companies.
- Clinical workflow vendors.
- Health-data infrastructure companies.
- AI application companies seeking a privacy-conscious medical-document workflow.

No partnership, acquisition interest, or commercial relationship is claimed.

## 12. Business models

Possible models include:

- Privacy-conscious consumer subscription.
- B2B per-seat or per-organization licensing.
- White-label/API licensing.
- Usage-based document processing, where economics and safety controls support it.

Pricing and willingness-to-pay require market validation.

## 13. Competitive advantages

Potential advantages are currently architectural/workflow advantages rather than proven moats:

- Conservative evidence-preserving extraction rather than opaque free-form output.
- Explicit owner-scoped report boundaries.
- Safety-conscious product positioning.
- Vendor-neutral seams for AI, retrieval, billing, storage, and telemetry.
- Small infrastructure footprint and understandable codebase.
- Synthetic test foundation and unusually candid documentation of limitations.

A buyer should assume that core technical concepts are reproducible and should seek defensible workflow, data rights, distribution, or customer relationships before treating the product as a durable moat.

## 14. Remaining risks

Material remaining risks include:

- **No verified customer traction.** No customers, revenue, or retention are claimed or verified.
- **No clinical validation.** No clinical validation or regulatory assessment has been completed.
- Production infrastructure and operational evidence are incomplete.
- No live payment-provider integration.
- OCR and broad document-layout coverage remain incomplete.
- Medical RAG is a foundation rather than a populated/evaluated production system.
- Third-party dependency/model/data licence inventory still requires formal diligence.
- Repository licensing and contributor/IP rights require legal review.
- Browser accessibility/responsive release testing remains to be completed at staging level.
- Legal/privacy documentation and market-specific compliance work remain.

## 15. Future roadmap

### Engineering

- Managed database/private object storage.
- Versioned migrations.
- Isolated asynchronous extraction workers.
- Malware scanning and production monitoring.
- Stronger session lifecycle and account recovery.

### Product/AI

- OCR evaluation.
- Broader synthetic extraction benchmark.
- Curated, versioned, licence-reviewed knowledge sources.
- Evidence-grounded educational explanations after safety evaluation.
- Human-factors and clinical review.

### Commercial

- Payment-provider integration with verified webhooks.
- Customer discovery and pricing validation.
- Production web client if Streamlit is no longer appropriate.
- Support, incident, privacy, and operational processes.

## 16. What a buyer receives

Subject to a definitive agreement and formal IP/legal diligence, the technical asset consists of the repository source code, tests, documentation, extraction workflow, authentication/authorization boundaries, operational foundations, deployment artifacts, and roadmap.

The buyer does **not** receive or inherit any claim of:

- Users
- Revenue
- Patents
- Exclusive datasets
- Clinical validation
- Regulatory clearance
- Compliance certification
- Provider agreements
- Partnerships
- Guaranteed commercial value

Those items do not exist merely because the code documents a potential path to them.

## 17. Acquisition-readiness assessment

The repository is materially more useful to a technical buyer when its boundaries are explicit: what works, what is tested, what is deliberately disabled, what depends on deployment infrastructure, and what requires non-engineering validation.

A buyer considering a six-figure acquisition should still require a live technical demonstration, independent security review, dependency/IP inventory, deployment evidence, product/customer evidence, and legal diligence before assigning that valuation.

**Bottom line:** MediQuery is an acquisition candidate only as an engineering/product foundation today. A $150,000 purchase price is **not justified by this repository alone**; it becomes a question of demonstrated differentiated IP/workflow, validated product demand, clean rights, and operational/clinical readiness that must be established outside the codebase.
