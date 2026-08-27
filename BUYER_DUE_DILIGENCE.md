# MediQuery — Buyer Due Diligence

## Executive question

### Why would a buyer pay $150,000 instead of building this themselves?

Today, the honest answer is: **the repository alone does not justify $150,000**.

A buyer can reproduce a basic upload/extraction application with commodity frameworks and models. The potential acquisition value comes from the accumulated engineering work around a focused medical-document workflow: authenticated ownership boundaries, conservative evidence-preserving extraction, structured schemas, deletion paths, usage entitlements, privacy-conscious telemetry, retrieval contracts, tests, deployment documentation, and a deliberately documented path toward a commercial product.

A six-figure valuation becomes more credible only if those assets are combined with validated differentiated workflow/IP, clean intellectual-property rights, measurable customer demand, production evidence, and appropriate clinical/privacy validation.

## Current maturity

| Area | Current position | Buyer interpretation |
| --- | --- | --- |
| Core API | Implemented | Useful foundation |
| Authentication/authorization | Implemented and tested | Stronger than an unauthenticated demo |
| Report extraction | Conservative structured pipeline | Useful but not universal/clinically validated |
| Storage/deletion | Local implementation | Production infrastructure still required |
| RAG | Retrieval foundation | Not a production medical knowledge system |
| Generative AI | Not enabled in protected report flow | Avoids unsupported clinical claims |
| Billing | Entitlement/metering seam | Payment integration remains |
| Observability | Aggregate/privacy-conscious foundation | Managed operations remain |
| Testing | API/unit/security-oriented suite | Browser/provider/release testing remains |
| UX | Functional Streamlit client | Commercial web UX remains an opportunity |
| Traction | None claimed | Major commercial risk |
| Compliance | None claimed | Legal/compliance diligence required |

## Technical risks

### 1. Architecture/product surface

The current system is deliberately small, but that also means some capabilities expected from a mature SaaS are absent: managed infrastructure, versioned database migrations, robust background processing, production-grade session lifecycle, and browser-level release testing.

**Technical response:** keep the architecture modular and add only the infrastructure justified by measured product requirements.

### 2. Document extraction

The extractor is intentionally conservative. It should not be interpreted as supporting every laboratory layout, table, language, unit convention, or OCR scenario.

**Technical response:** establish a synthetic benchmark covering representative layouts and measure precision/recall before expanding functionality.

### 3. Scalability

The local architecture is suitable for development and controlled workloads, not evidence of horizontal production scale.

**Technical response:** move document processing to isolated asynchronous workers, use managed database/object storage, and establish load/latency budgets before scaling.

## Security risks

Current source-level controls are documented in `SECURITY.md`, but real deployment requires provider-level controls, secret management, TLS/WAF, malware scanning, monitoring, backup/restore testing, and independent security assessment.

Per-process rate limiting and local storage are not substitutes for distributed controls in a multi-replica deployment.

**Buyer action:** require a threat model, penetration test, deployment configuration review, dependency/SBOM scan, secret review, and incident-response evidence.

## Legal and privacy risks

The product handles potentially sensitive health information. Technical safeguards alone do not establish a lawful or compliant processing operation.

Open questions include:

- Applicable jurisdiction(s).
- Controller/processor roles.
- Privacy notice and consent requirements.
- Data retention and deletion policy.
- Data residency.
- Vendor data-processing terms.
- Backup deletion policy.
- Cross-border processing.
- Regulatory classification, if any.
- Required healthcare agreements.

**Buyer action:** obtain specialized privacy, healthcare, and regulatory counsel before processing real patient data.

## Compliance risks

The repository makes **no** HIPAA, PIPEDA, PHIPA, GDPR, SOC 2, or other compliance claim.

A buyer should treat compliance as an environmental/organizational diligence item rather than a property of the source code.

## AI risks

The principal AI risk is overclaiming. The current protected workflow intentionally avoids treating free-form model output as medical fact.

Future generative/RAG features introduce risks including hallucination, unsupported diagnosis, prompt injection through documents, retrieval poisoning, incorrect citations, stale knowledge, and unsafe urgent-situation messaging.

**Technical response:** require source provenance, bounded retrieval, tenant isolation, adversarial tests, citation verification, model/version tracking, and clinical/human-factors review before activation.

## Infrastructure risks

The repository does not demonstrate:

- Production uptime.
- Disaster recovery.
- Tested restore procedures.
- Managed object storage lifecycle.
- Multi-region strategy.
- Production alerting.
- Distributed tracing.
- Production capacity limits.

**Buyer action:** inspect the actual staging/production environment rather than relying on Compose or documentation.

## IP risks

The repository currently has no general open-source licence grant. A buyer must establish:

- Contributor ownership and assignment.
- Dependency licences.
- Model licences.
- Dataset/source licences.
- Medical-content provenance.
- Trademark conflicts.
- Any copied/generated code obligations.
- Historical repository provenance and removed artifacts.

**Acquisition blocker:** rights must be clean enough to transfer.

## Business risks

No users, revenue, partnerships, retention, or market validation are claimed. A technically strong foundation can still have zero commercial value if customers do not want the workflow or acquisition costs are uneconomic.

**Response:** validate willingness to pay and retention before treating the codebase as a six-figure asset.

## Competitive risks

Most individual technical components are commodity capabilities. Authentication, PDF parsing, vector retrieval, LLM APIs, and web frameworks are readily available.

A defensible position therefore needs to come from a differentiated workflow, proprietary legally obtained data, distribution, integrations, customer relationships, or validated operational know-how—not from simply using AI.

## Acquisition blockers

A serious buyer should consider the following blockers until evidence is supplied:

1. Clean IP/contributor/licence package.
2. Production deployment evidence.
3. Security assessment and threat model.
4. Privacy/legal review for the target market.
5. Clinical/product validation appropriate to the intended claims.
6. Reliable extraction evaluation.
7. Verified customer demand and commercial traction.
8. Payment and operational readiness if a paid SaaS is intended.

## What can be fixed technically

- Extraction benchmarks and parser coverage.
- Background processing and resource isolation.
- Managed storage/database integration.
- Session lifecycle and account recovery.
- Browser accessibility/responsive testing.
- Production monitoring and alerting integrations.
- Payment-provider integration.
- Curated RAG evaluation infrastructure.

## What cannot be fixed by code alone

- Customer demand.
- Revenue and retention.
- Clinical validation.
- Legal rights and contracts.
- Regulatory determinations.
- Provider agreements.
- Security assurance independent of implementation.
- A defensible market position.

## Buyer diligence checklist

### Before signing

- [ ] Confirm seller identity and IP ownership.
- [ ] Review contributor history and assignments.
- [ ] Inventory dependencies/models/data sources and licences.
- [ ] Inspect Git history and release artifacts.
- [ ] Review secrets history and credential rotation.
- [ ] Review architecture and threat model.
- [ ] Review test results and coverage gaps.
- [ ] Run an independent security assessment.

### Before production use

- [ ] Deploy managed Postgres.
- [ ] Deploy private encrypted object storage.
- [ ] Configure TLS/WAF and distributed rate limiting.
- [ ] Implement malware scanning and isolated processing.
- [ ] Implement migrations/backups/restore testing.
- [ ] Configure managed monitoring and alerts.
- [ ] Complete privacy/compliance/legal review.
- [ ] Complete extraction/AI evaluation.
- [ ] Complete browser accessibility and UX testing.

### Before assigning a $150k valuation

- [ ] Evidence of customer demand.
- [ ] Evidence of willingness to pay.
- [ ] Clean transferable IP.
- [ ] Differentiated product/workflow.
- [ ] Demonstrable operating reliability.
- [ ] Credible path to margin and scale.
- [ ] Clear buyer-specific strategic value.

## Bottom line

MediQuery is a credible **engineering foundation**, not a proven $150,000 business today. The strongest acquisition thesis is that a buyer can acquire a disciplined starting point and accelerate productization, validation, and commercialization.

The project should be valued according to evidence. The repository intentionally avoids manufacturing evidence that does not exist.
