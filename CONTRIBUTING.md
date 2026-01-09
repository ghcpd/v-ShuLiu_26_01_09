# Contributing to Todo API Service

Thank you for your interest in contributing to the Todo API backend!

This document describes the intended contribution process.

## Branching & Workflow (Intended)

- Default branch: `main`
- Feature branches: `feat/<short-description>`
- Bugfix branches: `fix/<short-description>`
- Hotfix branches for production incidents: `hotfix/<incident-id>`

All pull requests **should**:

- Target `main`
- Be associated with at least one issue
- Have at least one approval from `@backend-core`
- Pass CI (tests + lint) before merge

## Issues

When opening an issue, please:

- Use the appropriate template (bug report, feature request, incident postmortem draft)
- Apply at least one **area** label:
  - `area:api`
  - `area:db`
  - `area:infra`
- For bugs and incidents, also add severity:
  - `sev1`, `sev2`, `sev3`

> In practice, some older issues use different label schemes (e.g., `type:bug`, `defect`, `priority-high`). We are **gradually normalizing** labels.

## Pull Requests

- Small, focused PRs are preferred
- Each PR **should** link to one or more issues with `Fixes #<id>` or `Refs #<id>`
- Breaking API changes **must** be documented in docs/api_versioning.md and in RELEASE_NOTES (if applicable)

Review expectations (intended):

- Backend changes: reviewed by `@backend-core`
- Deployment/infra changes: reviewed by `@sre` or `@platform`

## Incidents & Oncall

- Sev1 incidents **must** have a follow-up issue labeled `incident` and `sev1`
- A post-incident review should be added to ops/incidents.md
- Oncall rotation details live in ops/oncall.md (may be slightly out of date)

## Code Style & Testing (Simplified)

- Prefer FastAPI patterns (path operations in routers, Pydantic models)
- Tests for new endpoints go under tests/api/
- Use `pytest` for testing


