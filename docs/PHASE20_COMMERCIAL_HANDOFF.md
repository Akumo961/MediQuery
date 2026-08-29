# Phase 20 — Commercial Handoff & Release Candidate

## Purpose

Phase 20 is the final repository-level gate for turning MediQuery into a credible **technical acquisition / commercial handoff package**.

It does not manufacture customers, revenue, clinical validation, regulatory approval, compliance certification, or production infrastructure evidence. Instead, it makes the current engineering asset easy for a buyer or product team to inspect, reproduce, evaluate, and transfer into the next stage of commercialization.

## Acceptance criteria

1. Phases 17, 18, and 19 remain represented by their phase documents, tests, and CI workflows.
2. The repository contains an explicit commercial handoff document and release checklist.
3. `ACQUISITION.md` and `BUYER_DUE_DILIGENCE.md` remain part of the handoff package.
4. The README identifies the implemented workflow, safety boundary, technical limitations, and commercial limitations without overstating them.
5. The repository contains no committed local database, private upload directory, environment secret, or credential-shaped private key.
6. The handoff package explicitly separates implemented engineering assets from future work and external diligence.
7. The package includes a reproducible buyer demonstration path using synthetic data only.
8. The package explicitly identifies IP/licence review, dependency/data provenance review, security review, privacy/legal review, clinical review, deployment evidence, and customer validation as external diligence items.
9. CI executes this Phase 20 acceptance suite independently of the general quality suite.

## Buyer handoff package

A technical buyer should receive:

- source repository and Git history;
- architecture and trust-boundary documentation;
- security and medical-AI safety documentation;
- production-readiness documentation;
- synthetic tests and buyer demonstration workflow;
- deployment guidance and operational boundaries;
- acquisition overview and buyer due-diligence checklist;
- release checklist and the exact CI evidence for the transferred revision.

## Demonstration boundary

The buyer demonstration must use synthetic reports only. The demonstrable workflow is:

1. Create an account and acknowledge the medical limitations.
2. Upload the synthetic text-based PDF.
3. Verify extracted values, units, ranges, flags, pages, and source evidence.
4. Verify owner isolation with a second account.
5. Delete the report and verify it is no longer available to the owner.
6. Verify invalid PDF rejection.
7. Verify server-side Free-plan entitlement enforcement.
8. Verify retrieval provenance and prompt-injection framing.

## Commercial truthfulness boundary

Phase 20 does **not** claim:

- paying customers;
- revenue or retention;
- a guaranteed acquisition price;
- patents or exclusive intellectual property;
- clinical accuracy or clinical validation;
- medical-device or regulatory clearance;
- HIPAA, PIPEDA, PHIPA, GDPR, SOC 2, or equivalent certification;
- production PHI authorization;
- live payment processing;
- production uptime/SLA;
- managed cloud deployment;
- a populated production medical knowledge base.

A buyer may assign value to the engineering asset, but valuation remains an external commercial question supported by evidence beyond source code.

## External diligence required before closing

- Confirm seller identity and transferable IP ownership.
- Review contributor history and assignments.
- Inventory dependency, model, dataset, and medical-content licences.
- Review repository history for secrets and sensitive artifacts.
- Perform independent security/threat-model review.
- Review target-market privacy, healthcare, and regulatory obligations.
- Validate extraction quality on representative data.
- Validate customer demand and willingness to pay.
- Review deployment architecture, backups, restore procedures, monitoring, and incident response.
- Execute definitive transaction, confidentiality, IP-transfer, and other required legal agreements.

## Release evidence

Phase 20 is technically accepted when:

- the Phase 20 integrity gate passes;
- `tests/test_phase20_commercial_handoff.py` passes;
- the complete repository quality gate passes;
- the Phase 17, Phase 18, and Phase 19 gates pass;
- the resulting commit is the exact revision presented to a buyer.

## Final status

Phase 20 closes the **repository engineering program**. It does not close the external work required for a real medical-data launch or a completed acquisition transaction.
