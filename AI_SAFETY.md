# Medical AI safety

## Product boundary

MediQuery organizes detectable report text for education and discussion with a qualified clinician. It is not a diagnostic device, doctor replacement, emergency service, or clinically validated interpretation engine.

## Implemented safeguards

- The report pipeline produces structured candidates (name, value, unit, reference range, explicit flag, page, evidence) instead of asserting a free-form medical conclusion.
- Values and ranges are retained as extracted strings; no threshold is inferred when a range/flag is absent.
- The UI labels candidates as extracted material and tells users to verify them against the original report.
- Scanned/unreadable reports return an explicit limitation rather than fabricated results.
- The unsafe fixed-output vision endpoints are not mounted in the current API. No clinical image finding is represented as real analysis.
- PubMed failures return no results; the previous fabricated fallback papers were removed.

## Planned AI/RAG controls

If an AI explanation feature is enabled, it must use versioned, licence-reviewed sources and return source IDs/URLs next to each educational claim. Patient report text must be handled as untrusted data inside delimiters, never as instructions. Retrieval must be tenant-scoped for patient data, score-filtered, token-bounded, and evaluated against prompt-injection, hallucination, citation, and urgent-situation test sets.

Urgent language should direct users to local emergency services or a qualified clinician based on a reviewed policy, without attempting triage or diagnosis. Any deployment also needs clinical, legal, and human-factors review plus ongoing evaluation and incident handling.

## Retrieval foundation

`src/services/retrieval.py` enforces mandatory source identity, publisher, URL, version, and licence metadata; chunks content at sentence boundaries; relevance-filters and deduplicates results; and produces attribution alongside a bounded context that labels source text as untrusted data. It is a reusable contract, not a populated medical knowledge base or a live model integration.

## Known limitations

The deterministic parser is deliberately conservative but is not a medical-lab parser for all layouts, units, languages, tables, or reference conventions. It cannot validate the clinical correctness of a report, calculate risk, detect every abnormality, or replace original-document review. No RAG or generative-report explanation is currently enabled in the protected report flow.
