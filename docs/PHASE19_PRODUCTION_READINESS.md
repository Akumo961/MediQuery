# Phase 19 — Production Readiness Gate

## Purpose

Phase 19 establishes a repeatable release gate for MediQuery's production-shaped deployment boundary. It does **not** claim that the repository is approved for real patient/PHI processing, regulatory compliance, clinical validation, or a managed production SLA.

The gate verifies that unsafe development configuration cannot silently be treated as production configuration and that the documented release boundary remains explicit.

## Acceptance criteria

1. Production configuration must reject the development JWT secret.
2. Production configuration must reject JWT secrets shorter than 32 characters.
3. Production configuration must reject SQLite as the production database.
4. Production CORS origins must use HTTPS.
5. A configured metrics token must be at least 32 characters.
6. The deployment documentation must require private storage, managed database infrastructure, TLS/WAF, secret management, backups/restore testing, malware scanning, monitoring, and provider/legal review before PHI processing.
7. The repository must retain automated tests for authentication, tenant isolation, report deletion, medical AI safety, and extraction provenance.
8. CI must execute the Phase 19 acceptance tests independently of the general test suite.

## Explicit non-goals

Phase 19 does not implement or represent as complete:

- PHI/compliance certification;
- HIPAA, PHIPA, PIPEDA, GDPR, SOC 2, or equivalent certification;
- clinical validation or regulatory clearance;
- live payment processing;
- managed cloud provisioning;
- a versioned database migration service;
- a production SLA or disaster-recovery certification.

Those require deployment, legal, security, clinical, and operational evidence outside this repository.

## Release evidence

A Phase 19 release is considered technically accepted when:

- the Phase 19 test module passes;
- the complete repository test suite passes;
- Python compilation succeeds;
- the Phase 19 CI integrity gate passes;
- no production secret or local database is committed.

## Operational handoff

Before any real medical-data launch, the deployment owner must complete the remaining environment-level controls documented in `DEPLOYMENT.md`, including managed Postgres, private encrypted object storage, TLS/WAF, secret management, backups and restore testing, malware scanning, monitoring, access controls, and appropriate provider/legal agreements.
