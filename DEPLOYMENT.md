# Deployment

1. Provision managed Postgres and private encrypted object storage in the approved region. Do not use the development SQLite/local-directory defaults for real reports.
2. Set `ENVIRONMENT=production`, a unique 32+ character `JWT_SECRET`, the managed `DATABASE_URL`, approved HTTPS `CORS_ORIGINS`, and a private `UPLOAD_ROOT` through a secret manager.
3. Build and deploy the API behind TLS, a reverse proxy/WAF, and provider network restrictions. Do not publicly expose databases, caches, dashboards, or storage buckets.
4. Run migrations (not yet implemented), configure backups/restore tests, object lifecycle policies, malware scanning, metric/error redaction, alerts, and provider agreements before accepting PHI.
5. Run tests, dependency scan, secret scan, and a manual mobile/accessibility pass in CI/release approval.

The included CI workflow verifies formatting, linting, tests, compilation, and common credential patterns. It does not deploy, provision cloud resources, scan container images, or perform a compliance review.

`docker compose up --build` is a local production-shaped smoke tool, not a complete production deployment. Its API service intentionally requires a real managed database URL and secrets; it does not provision insecure database defaults.
