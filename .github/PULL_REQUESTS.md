# Pull Requests Overview (Synthetic Archive)

This file sketches example PRs to highlight collaboration and decision-making patterns.

---

## PR #210: Add connection pooling and bump ORM version

**Labels:** backend, performance, refactor

**Base:** main

**Description:**
Refactors database access layer, adds connection pooling, and bumps the ORM to v2.0.

**Discussion (high level):**
- Reviewer A: "We should roll this out gradually via canary, not all-at-once"
- Maintainer: "We don't really have a documented canary process yet, let's just monitor logs after deploy"
- SRE: "Please at least coordinate with oncall"

**Status:** Merged

**Notes:**
- Shortly after this PR, Issue #101 (production 500s) was opened
- No explicit link from this PR to an incident postmortem

---

## PR #213: Tune DB timeouts and add retries

**Labels:** hotfix, incident, sev1

**Base:** main

**Description:**
Adjusts DB connection timeouts and adds retry logic to reduce transient failures on `GET /todos`.

**Discussion:**
- Oncall SRE: "Merging this directly to main with admin override; tests are flaky and we don't have time to stabilize them now"
- Another maintainer: "We should document this kind of exception somewhere (incident playbook?)"

**Status:** Merged (CI partially failing, merged via override)

---

## PR #215: Fix background worker stuck on stale tasks

**Labels:** bugfix, backend, incident

**Base:** hotfix/worker-stall

**Description:**
Fixes stale task processing logic in the background worker.

**Discussion:**
- SRE: "Do we need a formal incident here?"
- Backend lead: "Let's just reference this PR in the weekly ops sync notes"

**Status:** Merged

---

## PR #220: Introduce `/v2/todos` API

**Labels:** feature, api-breaking, area:api

**Base:** main

**Description:**
Introduces a `/v2/todos` endpoint with slightly different semantics and response shape.

**Discussion:**
- One reviewer: "Should we mark `/v1/todos` as deprecated in docs?"
- Author: "We agreed in the last architecture review to maintain both for 6 months, but I don't see it written down"
- Another: "API versioning ADR is still in draft; let's merge and update docs later"

**Status:** Open (Draft)

---

## PR #221: Update incident documentation

**Labels:** documentation, ops

**Base:** main

**Description:**
Attempts to align ops/incidents.md with how we actually handle sev levels and oncall processes.

**Discussion:**
- Comment: "This reflects what we did in the last few incidents, but differs from CONTRIBUTING.md. We need a decision on which is source of truth."

**Status:** Open
