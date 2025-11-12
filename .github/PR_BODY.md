Title: chore(ingest-validation): add ingest schema validation, factor catalog split, tests

This PR contains the ingest validation work and supporting maintenance tasks required to make the SultryAI codebase CI-friendly.

Summary of changes
- Add JSON Schema validation to `POST /ingest/event` (returns 400 on validation errors).
- Add tests for valid and invalid ingest payloads and persistence to SQLite.
- Replace deprecated FastAPI startup hook with lifespan handler to load the FactorCatalog.
- Add `schemas/factor.schema.json` and validate factor catalog at startup.
- Clean and split the large `factors_catalog_full.json` into per-domain files and generate `factors_catalog/index.json`.
- Add `scripts/check_max_lines.py` improvements and `scripts/split_large_factors.py` to keep files under CI line limits.
- Add `.gitignore` and remove committed `.venv` files from the repo index.

Checklist
- [x] Add JSON Schema validation to `POST /ingest/event`
- [x] Tests for valid/invalid ingest and persistence
- [x] Replace deprecated startup handler with FastAPI lifespan handler
- [x] Factor schema + catalog validation
- [x] Split factor catalog and add `index.json`
- [x] Add `.gitignore` and remove `.venv`
- [ ] Add Prometheus metrics (follow-up PR)
- [ ] Scaffold honeypot sensor modules (follow-up PR)

Notes
- The branch is `feature/ingest-validation`.
- CI workflow will run the split/validate/check scripts and `pytest`.
- There are follow-up items (metrics and honeypot stubs) that will be split into smaller PRs.

Please review and merge to `main` when ready.
