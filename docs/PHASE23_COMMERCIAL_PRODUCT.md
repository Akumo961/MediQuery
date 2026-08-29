# Phase 23 — Commercial Product & Accessibility

## Purpose

Phase 23 hardens the user-facing product contract for a commercial release while preserving the medical safety boundary.

## Acceptance criteria

- The primary user journey is explicit: signup, limitation acknowledgement, upload, review, and deletion.
- Interactive controls have accessible names, labels, and descriptions.
- Keyboard navigation and visible status/error states are covered by the UI contract.
- Responsive behavior is evaluated at supported viewport sizes before release.
- Authentication failures and destructive actions have clear user feedback.
- Free/Pro entitlement behavior is enforced server-side.
- Billing integrations, when enabled, use verified provider webhooks and idempotency.
- No client-side UI can bypass authorization or entitlement controls.
- Product copy never implies diagnosis, treatment, emergency guidance, or clinical validation.

## Evidence boundary

The repository contains an accessibility contract and tests. Browser certification, payment-provider accounts, production analytics, customer usability evidence, and market validation remain external evidence.

## Product rule

A polished interface must not weaken safety. Every medical-report screen should keep the educational/non-diagnostic boundary visible and preserve source evidence alongside extracted information.

## Exit condition

Phase 23 is repository-complete when the UI contract, product tests, accessibility checks, and CI gate pass. Commercial product-market fit is not established by passing software tests.
