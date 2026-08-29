# Phase 18 — Medical AI Safety

## Objective

Establish a deterministic, testable safety boundary for any future educational AI feature without enabling diagnosis, treatment, clinical decision support, or emergency triage.

## Implemented controls

- `src/core/medical_safety.py` provides a model-agnostic policy layer.
- Generated text containing diagnostic claims or treatment instructions is rejected.
- Urgent-situation language receives a fixed emergency-services/qualified-clinician handoff rather than automated triage.
- Report text and user questions are wrapped as untrusted data in a bounded prompt contract.
- Empty output is rejected.
- The policy is deterministic and unit-tested; it does not claim universal model safety.

## Required future AI contract

A production generative feature must:

1. receive only owner-authorized report data;
2. preserve report evidence and source identifiers;
3. use curated, licence-reviewed medical sources;
4. enforce bounded retrieval and attribution;
5. treat report and retrieved text as untrusted data;
6. run output policy checks before display;
7. refuse diagnosis, prescribing, dosing, medication-change instructions, and clinical triage;
8. provide an emergency handoff for reviewed urgent-language patterns;
9. log privacy-safe safety events without report text or sensitive content;
10. undergo human clinical, legal/privacy, security, and human-factors review before deployment.

## Test matrix

| Scenario | Expected behavior |
|---|---|
| Educational description supported by evidence | Allow |
| Diagnostic assertion | Block |
| Medication/dose instruction | Block |
| Medication start/stop instruction | Block |
| Empty generated response | Block |
| Reviewed urgent-language pattern | Fixed emergency handoff; no triage |
| Prompt-injection text inside report | Treat as data, never as instructions |

## Explicit non-claims

Phase 18 does not establish clinical accuracy, regulatory clearance, emergency detection accuracy, medical-device status, or safety against every possible adversarial prompt. The policy is a deterministic guardrail for a future AI boundary, not a substitute for clinical validation or professional review.

## Acceptance criteria

- [x] Deterministic medical-AI policy exists outside the UI.
- [x] Diagnosis and treatment instructions are blocked by automated tests.
- [x] Urgent language receives a fixed safety handoff without automated triage.
- [x] Untrusted report/question boundaries are explicit.
- [x] Phase-specific acceptance suite is defined in CI.
- [x] Limitations and required pre-deployment review are documented.
