# MediQuery — Release / Buyer Handoff Checklist

## Repository gate

- [ ] Pin the exact release commit SHA.
- [ ] `python -m black --check src tests app.py`
- [ ] `python -m flake8 src tests app.py --max-line-length=120`
- [ ] `python -m pytest -q`
- [ ] `python -m compileall -q src app.py`
- [ ] GitHub Actions quality gate is green.
- [ ] Phase 17 acceptance is green.
- [ ] Phase 18 acceptance is green.
- [ ] Phase 19 acceptance is green.
- [ ] Phase 20 acceptance is green.
- [ ] No local database, private uploads, `.env`, or credential-shaped secret is committed.

## Buyer demonstration

- [ ] Create account with synthetic data only.
- [ ] Upload synthetic text-based PDF.
- [ ] Verify structured findings and source evidence.
- [ ] Verify owner isolation with a second account.
- [ ] Verify report deletion.
- [ ] Verify invalid PDF rejection.
- [ ] Verify Free entitlement enforcement.
- [ ] Verify retrieval provenance and prompt-injection framing.

## Diligence package

- [ ] `ARCHITECTURE.md`
- [ ] `SECURITY.md`
- [ ] `AI_SAFETY.md`
- [ ] `TESTING.md`
- [ ] `DEPLOYMENT.md`
- [ ] `PERFORMANCE.md`
- [ ] `ACQUISITION.md`
- [ ] `BUYER_DUE_DILIGENCE.md`
- [ ] `docs/DEMONSTRABLE_DIFFERENTIATION.md`
- [ ] `docs/PHASE18_MEDICAL_AI_SAFETY.md`
- [ ] `docs/PHASE19_PRODUCTION_READINESS.md`
- [ ] `docs/PHASE20_COMMERCIAL_HANDOFF.md`

## External closing gates

- [ ] IP ownership and contributor rights verified.
- [ ] Dependency/model/data licences reviewed.
- [ ] Security/threat-model review completed.
- [ ] Target-market privacy/legal/regulatory review completed.
- [ ] Extraction quality independently evaluated.
- [ ] Customer demand and willingness to pay validated.
- [ ] Production deployment evidence reviewed.
- [ ] Transaction and IP-transfer agreements executed.

These external items are intentionally not represented as completed by repository CI.
