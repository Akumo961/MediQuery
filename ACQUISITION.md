# Acquisition overview

## Implemented

MediQuery now has a documented, lean foundation for authenticated, owner-scoped report uploads; structured evidence-preserving extraction; a safety boundary that avoids placeholder clinical claims; server-side plan entitlements and durable usage metering; protected operational telemetry; containerization; tests; and candid operating/security documentation. Billing is provider-neutral and does not fabricate payment success. Observability records request IDs, safe request latency/status metrics, product counters, upload failures, rate limiting, and billing events without using report text, filenames, tokens, or email addresses as metric dimensions.

The architecture remains deliberately vendor-neutral for managed storage, retrieval, AI, payment, and telemetry adapters. A future Stripe adapter can update the subscription state without changing entitlement logic.

## Phase 9 status

**Implemented:** free/pro plan definitions, report and AI request limits, durable usage events, idempotency keys, server-side enforcement, authenticated billing summary, and a checkout boundary that only returns a real configured URL.

**Not claimed:** live card charging, Stripe webhook reconciliation, invoices, refunds, tax handling, or a production payment-provider agreement. Those require a real provider account, credentials, webhook endpoint, and business/legal setup.

## Phase 10 status

**Implemented:** request IDs, structured safe request logging, aggregate counters, request/report latency measurements, failure counters, rate-limit counters, billing counters, and a metrics endpoint protected by an explicit collector token. The telemetry design forbids sensitive data dimensions.

**Not claimed:** managed log retention, distributed tracing, alert routing, uptime/SLO evidence, or a third-party observability account. Those are deployment-level integrations and require operational infrastructure.

## Potential

With validated extraction, curated-source RAG, a polished web client, managed production operations, and customer traction, MediQuery could become a focused patient-facing report-organization product or a white-label workflow component for clinics, benefits providers, labs, or health-navigation platforms. Possible models include a privacy-conscious subscription, B2B per-seat licensing, or API/white-label pricing.

## Buyer receives

The repository, code documentation, test foundation, deployment guidance, acquisition package, server-side monetization seam, and privacy-conscious operational telemetry. It does **not** demonstrate users, revenue, patents, exclusive data, clinical validation, provider agreements, or compliance certification.

## Remaining risks

A production launch still needs managed database/storage, a real payment provider and webhook reconciliation, managed observability/alerting, legal/privacy work, validated extraction/RAG evaluations, third-party licence inventory, clinical/product validation, and commercial traction. The repository history was cleaned before the current acquisition baseline; the local backup of the previous Git history should be retained until the new repository has been independently verified.
