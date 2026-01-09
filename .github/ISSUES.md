# Issues Overview (Synthetic Archive)

This file contains representative issues to illustrate collaboration and governance patterns.

---

## Issue #101: [BUG] `GET /todos` intermittently returns 500 in production

**Labels:** bug, incident, sev1, infra

**Description:**
We are seeing intermittent 500 errors on `GET /todos` in production. Error rate spikes during peak traffic.

**Notes:**
- Started around 2024-10-01 after deploying PR #210
- Logs show connection timeouts to Postgres

**Discussion (high level):**
- Oncall SRE applied a manual rollback in Kubernetes but did **not** revert the DB migration
- Later comments mention "we usually don't roll back DB migrations unless strictly necessary", but this is not codified in docs

**Status:** Closed

**Resolution:** Fixed in PR #213 by adjusting connection pooling and adding retries. Post-incident review added informally in comments, not in ops/incidents.md.

---

## Issue #102: [INCIDENT] Background worker stuck processing stale tasks

**Labels:** incident, sev-1, backend

**Description:**
Background worker processing recurring tasks got stuck and reprocessed the same tasks for several hours.

**Notes:**
- Severity label uses `sev-1` instead of `sev1`
- Oncall escalated in Slack, but escalation path is not reflected in any public doc

**Status:** Closed

**Resolution:** Fixed in PR #215. No formal postmortem recorded; comment says "we'll add this to the next incident review batch".

---

## Issue #103: [FEATURE] Support soft-deleting todos

**Labels:** enhancement, area:api, area:db

**Description:**
Add soft-delete semantics so clients can restore recently deleted todos.

**Discussion:**
- Some participants argue this is a breaking API change and should be versioned as `v2`
- Others suggest handling it as a non-breaking extension with an additional query parameter
- Reference to an "API versioning ADR" that is not easily discoverable

**Status:** Open

---

## Issue #104: [DOC] Clarify incident severity levels

**Labels:** documentation, help wanted

**Description:**
Our incident docs in ops/incidents.md mention `sev1`/`sev2`/`sev3`, but actual issues sometimes use `sev-1` or only `priority-high`.

**Status:** Open

---

## Issue #105: [QUESTION] Who approves schema changes?

**Labels:** question, area:db

**Description:**
It's not clear whether SRE or backend-core has final say on risky schema changes.

**Discussion:**
- One maintainer says: "In practice, whomever is oncall decides during incidents"
- Another: "For planned work, we decided in the last retro that backend-core leads, but I don't see it documented"

**Status:** Closed (after a brief answer in comments, no doc update)

---

## Issue #106: [BUG] `PATCH /todos/{id}` accepts invalid payloads

**Labels:** type:bug, area:api

**Description:**
Missing validation for some optional fields; invalid data can be stored.

**Status:** Open

---

## Issue #107: [ENHANCEMENT] Add tracing for background workers

**Labels:** enhancement, infra, help wanted

**Description:**
Add OpenTelemetry tracing to background workers so we can debug incidents easier.

**Status:** Open

---

## Issue #108: [META] Align label usage for bugs/incidents

**Labels:** enhancement, documentation, good-first-issue

**Description:**
We currently mix `bug`, `type:bug`, `defect`, `incident`, `priority-high`, and `sev1`/`sev-1` across issues. This makes reporting confusing.

**Status:** Open


