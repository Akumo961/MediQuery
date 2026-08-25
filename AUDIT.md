# MediQuery technical audit

**Audit date:** 2026-08-25  
**Scope:** Complete checked-out repository, Git metadata, tracked files, application source, notebooks, dependency manifests, and Docker Compose configuration. No code was changed before this document was created.

## Executive assessment

MediQuery is an early Python proof of concept, not yet a medical-report SaaS. Its runnable components are a FastAPI API, a Streamlit demo UI, PubMed lookup, local sentence-transformer ranking, PDF text extraction, and demonstrative vision responses. The repository contains no Next.js application, Gemini integration, Pinecone integration, persistent product database usage, authentication, user model, billing, report history, or production deployment implementation.

The current code must not be represented as clinically validated, secure for protected health information (PHI), compliant with any healthcare/privacy framework, or production-ready. The most material acquisition issue is not a lack of features: it is the large gap between product claims and implemented behaviour.

## 1. Critical issues

1. **Unauthenticated public PHI endpoints.** `/api/document/upload`, document QA, and vision endpoints accept files with no identity, ownership check, authorization, or consent record.
2. **Uploaded images are persisted and publicly served.** `src/api/main.py` mounts `/uploads`, while `vision.py` writes user uploads to it and returns the filesystem path. This can expose sensitive reports/images to anyone who can guess or obtain a URL.
3. **No effective upload safeguards.** There are no byte limits, content/MIME verification, image decompression limits, antivirus/malware scanning, PDF page/complexity limits, storage quotas, or cleanup/deletion workflow. Filename extensions are the principal checks.
4. **Hard-coded credentials and insecure services in `docker-compose.yml`.** Database, Redis, Grafana, Flower, and application secrets are committed defaults; several services are host-exposed, Elasticsearch security is disabled, and the referenced Dockerfiles/configs/init scripts are absent. These values must be considered compromised and must never be deployed.
5. **Medical vision functions fabricate results.** The `MedicalVisionModel` returns fixed X-ray/anomaly/VQA payloads, including a “Possible finding.” The Streamlit UI presents those values as analysis. This is a serious safety and product-integrity issue.
6. **No data lifecycle or privacy controls.** Reports can be retained indefinitely on the local filesystem; there is no report deletion, account deletion, retention schedule, encryption-key design, audit trail, or data-processing/provider inventory.

## 2. High-priority issues

1. Document extraction relies on `PyPDF2` alone and concatenates page text without preserving page boundaries, tables, units, reference ranges, provenance, or OCR state.
2. Document QA silently truncates source text to 1,000 characters, then reports model confidence without calibration or source citations. It can answer unsupported questions and is vulnerable to instructions embedded in reports.
3. Search substitutes fabricated sample papers when PubMed is unavailable. The UI labels them PubMed and displays invented authors/journals, which breaks source integrity.
4. The advertised maximum file sizes are not enforced. Vision uploads are copied synchronously to disk; PDFs have no file type verification or resource controls.
5. Errors are returned as raw exception text in several routes, leaking implementation details. Broad `except` blocks suppress operational failures.
6. CORS permits credentials and broad methods/headers without an authentication/session architecture or CSRF strategy.
7. Core models download/load synchronously at module import and use a general QA model, introducing startup, availability, memory, licensing/model-card, and safety risks.
8. The API has no rate limiting, request correlation, safe structured logging, health/readiness distinction, timeout budget, abuse controls, or observability.
9. The repository claims or implies unsupported capabilities: working multimodal medical analysis, clinical-data access, analytics, model accuracy/uptime, React frontend, Compose deployment, test coverage, and MIT licensing. `LICENSE` does not exist.
10. The Git repository tracks 52,306 virtual-environment files and has a roughly 502 MB packed history. This inflates clone size, embeds third-party code/artifacts, and creates IP/supply-chain diligence risk.

## 3. Medium-priority issues

1. The codebase uses ad-hoc import-path mutation, global singleton models, working-directory-relative paths, and duplicated vector-store abstractions.
2. FAISS is present but is not integrated into the product search flow. The code has no document schema, chunking pipeline, metadata contract, source ID, versioning, relevance threshold, tenancy filtering, or citation rendering.
3. PubMed caching writes query-based JSON files to local disk without a retention policy, cache bounds, provenance fields such as PMID/URL, or concurrency safeguards.
4. `VectorStore` persists unencrypted metadata and uses unsafe pickle in `EmbeddingManager`.
5. Image decoding is not validated before model processing; files are permanently retained after failures as well as successes.
6. No database tables, migrations, object-storage adapter, background job design, idempotency, queues, or retry policy are implemented despite Compose listing many services.
7. Streamlit CSS uses `unsafe_allow_html=True`; it mostly formats controlled text today, but this is an avoidable XSS footgun as user-controlled content evolves.
8. Mobile, keyboard, screen-reader, focus, colour-contrast, and semantic accessibility have not been tested. The UI is desktop/tab-demo oriented.
9. Dependency versions are old and tightly pinned; no lockfile, vulnerability scanning, SBOM, automated update process, or compatibility matrix exists.
10. No CI workflow, deployment manifests, Dockerfiles, health orchestration validation, environment template, or release process is present.

## 4. Low-priority issues

1. Unused imports, inconsistent formatting, missing return typing, and generic dictionary types reduce maintainability.
2. The React `package.json` is orphaned: no source, lockfile, or build configuration accompanies it.
3. Notebooks contain simulated performance/accuracy material that could be mistaken for measured production evidence.
4. The README contains a NUL byte in the working tree and is not reliably plain Markdown.
5. `.idea`, Python bytecode, local output folders, and a virtual environment appear in Git state; the current ignore configuration is deleted/modified and ineffective for them.

## 5. Missing capabilities

- Accounts, sessions, password reset, email verification, consent acknowledgement, role/tenant boundaries, and server-side authorization.
- Database-backed report lifecycle, encrypted object storage, report history, deletion, retention controls, export, and account deletion.
- Structured medical-report schema, deterministic lab-value extraction, abnormality rules, page-level evidence, OCR, human-readable processing errors, and manual correction.
- A safe AI orchestration boundary with documented model/provider configuration, grounded outputs, evidence citations, urgent-symptom handling, prompt-injection controls, and evaluation data.
- A real application dashboard and landing/onboarding flow; billing entitlement abstraction; support/contact workflow.
- Tests, CI, operational runbook, safe deployment configuration, monitoring/error reporting, backups/disaster recovery, and a dependency/license inventory.

## 6. Security risks

- Anonymous access plus public upload serving enables PHI disclosure.
- Default secrets, host-exposed stateful services, disabled Elasticsearch security, and weak Docker configuration enable compromise.
- No request/file limits creates denial-of-service exposure, including decompression and PDF parsing attacks.
- No authentication, authorization, CSRF protection, rate limit, audit logging, or account security controls.
- Raw exception leakage, unredacted logging potential, insecure pickle loading, and unverified external model downloads increase attack surface.
- No secret scanning or evidence that repository history is free of previously committed credentials. The Compose defaults should be rotated before any deployment.

## 7. Healthcare/privacy risks

- The architecture currently has no defensible PHI handling boundary or data-processing inventory.
- Document and image content may be stored locally, served publicly, sent to external model providers, or written into caches without notice or consent.
- Fixed vision “findings,” unlabeled extractive summaries, fabricated fallback literature, and ungrounded QA can mislead users about medical facts.
- There is no clinical validation, intended-use statement, adverse-event handling, auditability, or evidence of regulatory/legal review.

## 8. Architecture weaknesses

The application consists of a Streamlit client calling a local FastAPI process. The API imports heavyweight models directly, accesses local files, performs synchronous remote HTTP requests, and has no persistence or identity boundary. Compose describes a much larger system (Postgres, Redis, Elasticsearch, Weaviate, Celery, Prometheus, Grafana, Flower, Nginx) that the code neither configures nor uses fully; referenced build/config assets are missing. This creates a misleading and hard-to-operate architecture rather than scalable infrastructure.

## 9. Product weaknesses

The present UX focuses on generic literature search and simulated image analysis, not the stated medical-report workflow. It displays invented “Active Users,” accuracy, uptime, and analytics, which undermines buyer trust. There is no report history, source panel, user settings, plan model, or reliable onboarding. The product positioning must be narrowed to a clearly-disclaimed report-organizing/education tool until actual clinical validation exists.

## 10. Acquisition blockers

1. No proprietary or validated clinical asset is demonstrated; the vision layer is a placeholder.
2. No secure multi-user data architecture or evidence of real deployment operations exists.
3. No user, revenue, retention, customer, regulatory, or clinical-validation evidence is in the repository.
4. Repository hygiene, third-party licensing, credentials, and deployability require remediation.
5. Documentation currently overstates implementation and contains unsupported benchmark/production claims.
6. A buyer can reproduce much of the current prototype quickly from commodity components; value must come from a coherent, safe workflow, evaluations, operating evidence, and legitimate customer traction rather than the current code volume.

## Due-diligence conclusion

The appropriate immediate engineering plan is a deliberately small, secure report-analysis foundation: structured extraction with evidence, authenticated tenant-scoped storage, safe lifecycle controls, explicit AI safety boundaries, audited citations, tests, and truthful documentation. Placeholder medical-image diagnosis and unsupported production claims should be removed or clearly isolated before marketing the product.
