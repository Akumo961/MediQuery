# Phase 22 — AI, Retrieval & Evaluation

## Purpose

Phase 22 establishes a measurable evaluation layer for extraction and retrieval without presenting synthetic results as clinical validation.

## Acceptance criteria

- A versioned synthetic benchmark covers representative supported report layouts.
- Finding evaluation reports deterministic precision and recall.
- Retrieval evaluation measures source/citation coverage and relevance thresholds.
- Every knowledge source retains identity, publisher, URL, version, and licence metadata.
- Retrieved document text remains untrusted data and cannot become instructions.
- Prompt-injection, unsupported-claim, and insufficient-evidence cases are tested.
- Model/provider integrations remain replaceable and are disabled unless explicitly configured.
- No generated output is represented as diagnosis, treatment advice, or clinical decision support.

## Evidence boundary

Phase 22 produces engineering measurements. It does not establish clinical accuracy, medical-device performance, regulatory clearance, or suitability for real patient care. Clinical validation requires representative data, an approved protocol, qualified reviewers, and independent evidence.

## Evaluation contract

`src/services/evaluation.py` provides deterministic finding comparison and retrieval grounding coverage. These metrics are intentionally narrow: they measure whether an implementation matches an expected synthetic representation, not whether a medical conclusion is clinically correct.

## Exit condition

The repository phase is complete when the synthetic evaluation suite, retrieval safety tests, documentation, and CI gate pass. Production medical AI activation remains subject to external clinical, legal, privacy, and safety review.
