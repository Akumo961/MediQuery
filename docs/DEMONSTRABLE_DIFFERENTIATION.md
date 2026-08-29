# Phase 17 — Demonstrable Differentiation

## Objective

Turn MediQuery's existing engineering choices into **demonstrable, testable product differentiation** without inventing clinical capability, proprietary data, customers, revenue, or regulatory status.

Phase 17 is complete when a technical buyer can reproduce the claims below from source code, tests, or a documented local demonstration.

## Differentiation pillars

| Pillar | What is demonstrable | Evidence in repository | Boundary |
|---|---|---|---|
| Evidence-first extraction | Findings retain value, unit, reference range, explicit flag, page and source evidence | `src/services/report_analysis.py`, report tests | Extraction is not clinical interpretation |
| Conservative failure handling | Invalid/encrypted/oversized PDFs and unreadable text fail closed or surface a limitation | `report_analysis.py`, API tests | OCR is not implemented |
| Owner isolation | Report queries are scoped to the authenticated owner | `src/api/routes/reports.py`, security tests | Deployment still requires production identity/session controls |
| Privacy-conscious storage | Storage keys are generated from owner/report IDs and are not public URLs | `reports.py`, security/deployment docs | Production requires private managed storage |
| Safety boundary | Product language and API contracts distinguish organization from diagnosis/medical advice | `app.py`, `AI_SAFETY.md`, schemas | No clinical validation is claimed |
| Provenance-ready retrieval | Knowledge chunks require source identity, publisher, URL, version and licence metadata | `src/services/retrieval.py`, retrieval tests | No production medical corpus is bundled |
| Prompt-injection resistance | Retrieved prose is framed as untrusted data and context is bounded | `retrieval.py` | This is a control, not proof of universal model safety |
| Vendor-neutral monetization | Plans, entitlements and usage metering are independent of a payment provider | `src/core/billing.py`, billing tests | Live payment execution/webhooks are not implemented |
| Operational privacy | Aggregate metrics avoid report text, filenames and sensitive dimensions; request IDs and rate limiting are present | `src/core/observability.py`, `src/api/main.py`, platform tests | Production observability still needs deployment validation |

## Buyer demonstration script

A buyer or reviewer can demonstrate the core workflow locally:

1. Create an account and acknowledge the medical limitations.
2. Upload the synthetic text PDF.
3. Confirm the four extracted findings preserve values, units, ranges, flags and page numbers.
4. Open source evidence and compare every finding with the original report.
5. Create a second account and verify the first account's report is inaccessible.
6. Delete the report and verify it disappears from the owner's report list.
7. Attempt invalid PDF upload and verify it is rejected.
8. Exercise the Free entitlement and verify the server—not the UI—enforces the report allowance.
9. Exercise retrieval primitives with a source containing hostile instruction-like prose and verify it remains framed as untrusted reference data.

## What makes the asset differentiated

The strongest current differentiator is **the combination of controls**, not any individual algorithm: source-preserving extraction + owner-scoped data boundaries + conservative failure behavior + provenance contracts + provider-neutral seams + explicit safety limitations.

These properties make the codebase easier to validate and extend than a generic chatbot prototype while keeping unsupported clinical claims out of the product.

## What is deliberately not claimed

Phase 17 does not claim:

- diagnostic accuracy;
- clinical decision support;
- regulatory approval or certification;
- HIPAA/PIPEDA/PHIPA/GDPR compliance certification;
- proprietary medical datasets;
- customer traction, revenue or retention;
- patents or exclusive IP;
- production medical RAG quality;
- a live payment provider;
- a production SLA.

Those require external evidence and diligence.

## Commercial implication

The repository can be presented as a **defensible engineering foundation for a medical-document workflow**, but code alone does not establish a six-figure valuation. A buyer should separately validate IP ownership, dependency/data licences, security, clinical/regulatory requirements, customer demand, deployment readiness and economics.

## Phase 17 acceptance criteria

- [x] Differentiation pillars are explicit.
- [x] Each pillar has repository-level evidence.
- [x] Unsupported claims are explicitly excluded.
- [x] A repeatable buyer demonstration is documented.
- [x] Automated acceptance tests cover the key architectural claims.
- [x] CI executes the Phase 17 acceptance suite.
