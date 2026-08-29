# Phase 21 — Production Infrastructure

## Purpose

Phase 21 converts the production-shaped repository into an explicit, fail-closed deployment contract. It does not claim that MediQuery has a live managed production environment.

## Acceptance criteria

- Managed PostgreSQL is mandatory for production.
- Private encrypted object storage is mandatory for report artifacts.
- TLS and WAF protection are mandatory at the edge.
- Secrets must come from a managed secret manager and support rotation.
- Document processing must be isolated and asynchronous before real sensitive-data scale.
- Uploads require malware scanning and resource limits.
- Backups must have tested restore procedures.
- Health/readiness and aggregate monitoring must be available without exposing report content.
- Production configuration uses a fail-closed policy instead of silently using SQLite or development secrets.

The production contract **fails closed** when a mandatory control is missing; the application must not silently fall back to insecure development configuration.

## Fail closed

Production must **fail closed** whenever a mandatory infrastructure or security control is unavailable or misconfigured. The application must reject the production configuration rather than silently falling back to SQLite, development secrets, insecure storage, or other non-production defaults.

## Evidence boundary

The repository provides a machine-testable `ProductionRequirements` contract. Managed accounts, provider configuration, backup exercises, uptime history, and real PHI authorization remain external evidence and are not represented as completed by source code alone.

## Operational sequence

1. Provision managed database and private object storage.
2. Configure secret manager and rotation.
3. Place TLS/WAF in front of the API.
4. Run isolated extraction workers with CPU, memory, time, and file-size limits.
5. Scan uploads before processing.
6. Enable backups and perform a documented restore test.
7. Configure aggregate monitoring and incident alerts.
8. Execute staging smoke and rollback tests before production promotion.

## Exit condition

Phase 21 is repository-complete when the contract, documentation, and acceptance tests pass. Real production deployment remains an external operational activity.
