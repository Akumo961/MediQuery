# MediQuery — Final Security Audit Scope

## Scope

This document records the final repository-level security posture for the current release. It is not an independent penetration-test certificate.

## Controls reviewed

- Authentication and password verification.
- JWT expiration/type handling and production secret validation.
- Owner-scoped report authorization.
- Cross-owner report access behavior.
- Upload extension/MIME/magic-byte/size/encryption/parser validation.
- Server-generated storage paths.
- SQLAlchemy parameterized persistence.
- Security response headers and CORS configuration.
- Rate-limit middleware and retry signaling.
- Safe API error responses.
- Account/report deletion behavior.
- Credential-shaped secret scanning in CI.
- Removal of unreachable ML/retrieval prototypes and unused frontend package metadata.

## Residual risks requiring buyer/environment controls

1. Local SQLite is for development; production requires managed PostgreSQL.
2. Local filesystem uploads are not a production object-storage architecture.
3. CI Docker validation does not constitute a production penetration test.
4. Distributed rate limiting is required for multi-replica deployment.
5. Malware scanning and isolated document processing remain deployment requirements.
6. Backup retention/deletion must be implemented and tested operationally.
7. Privacy, regulatory, and clinical reviews remain external requirements.

## Security conclusion

The source repository contains a credible application-level security foundation for the intended educational/document-organization scope. It must not be represented as a completed compliance certification or independent security assessment.

## Release rule

Do not enable real patient-data processing solely because the repository tests pass. Production enablement requires buyer-specific infrastructure, privacy, security, clinical, legal, and regulatory acceptance.
