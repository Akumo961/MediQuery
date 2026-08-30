# MediQuery — 3-Minute Buyer Video Script

## 0:00–0:20 — Problem

“Medical reports arrive as documents. MediQuery turns a text-based PDF into structured, reviewable findings while preserving source evidence and enforcing authenticated ownership boundaries.”

## 0:20–0:45 — Login

Show signup/login and the medical-limitations acknowledgement. Explain that protected report access requires authentication.

## 0:45–1:20 — Upload and processing

Upload a synthetic laboratory PDF. Show Hemoglobin, WBC, and Platelets. Point out the `10^3/uL` units used by common CBC reports.

Say: “The current release deliberately uses deterministic extraction rather than claiming clinical AI.”

## 1:20–1:55 — Evidence

Show the extracted value, unit, reference range, flag, page number, and source-derived evidence. Compare the result to the original synthetic PDF.

## 1:55–2:25 — Security

Show report history/detail and, if prepared, a second demo account attempting to access the first account's report. Show denial. Explain owner-scoped authorization.

## 2:25–2:45 — Account deletion

Delete the demo account. Show that the old credentials no longer authenticate.

## 2:45–3:00 — Acquisition proposition

“MediQuery is offered as a health-tech software/IP asset: a working secure document workflow with deterministic extraction, evidence preservation, tests, Docker deployment shape, security controls, and buyer documentation. It is not being represented as a certified medical device or autonomous clinical AI.”

## Recording rules

- Synthetic data only.
- No patient-identifiable information.
- Do not display secrets, tokens, database credentials, or private infrastructure.
- Use the exact release commit intended for buyer review.
- Keep the demo reproducible from the repository documentation.
