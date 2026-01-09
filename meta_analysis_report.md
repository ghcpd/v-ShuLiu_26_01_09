# Meta-analysis: Collaboration & Ops for Todo API Service

## Summary
The repository contains clear, intended processes (CONTRIBUTING.md, docs/api_versioning.md, ops/oncall.md) but real practice often diverges: incidents are sometimes resolved by urgent hotfixes and Slack coordination rather than by the documented GitHub-first process. This report highlights where rules are defined, how they are actually followed, and what a new backend engineer or SRE must know.

## What the docs prescribe
- Contribution and review rules live in `CONTRIBUTING.md` (branch naming, approval by `@backend-core`, CI before merge) and review expectations split backend vs SRE reviews.
- Incident and oncall expectations (response SLAs, create an `incident`-labeled issue, post-incident review) are recorded in `ops/oncall.md` and `ops/incidents.md`.
- API versioning guidance is drafted in `docs/api_versioning.md` (introduce `/v2`, keep `/v1` for a deprecation window).
- Label conventions are described in `.github/LABELS.md` (area, severity, status labels).

## Observed practice (evidence)
- Hotfixes and emergency merges happen in the wild: PR #213 was merged as a hotfix and explicitly notes an "admin override" while CI was partially failing (see `.github/PULL_REQUESTS.md` entry for PR #213). PR #215 is another hotfix merged to address a background-worker issue.
- Incidents are inconsistently logged: `ops/incidents.md` records the 2024-10-01 `GET /todos` Sev1 outage linked to PR #210 and the follow-up PR #213, but it also notes that "Some discussion happened in Slack and was not fully copied here." The 2024-11-12 worker stall was tracked in Issue #102 and fixed by PR #215, yet postmortem coverage was incomplete.
- Labels and severities are uneven: the repo uses multiple formats (`sev1`, `sev-1`, `priority-high`) as called out in `.github/LABELS.md` and `ops/incidents.md` (the worker-stall incident is described as "Sev1" in notes but the GitHub issue used `sev-1`).
- API-breaking changes are sometimes merged before governance is fully formalized: PR #220 introduces `/v2/todos` while `docs/api_versioning.md` still lists open questions about who authorizes breaking changes.
- The project maintains milestone context (`.github/MILESTONES.md`) tying incidents to issues (e.g., #101, #102), but the chain from PR → incident → formal postmortem is not consistently complete (see PR #210 → Issue #101 and the note that no separate postmortem issue existed at the time).

## Key inconsistencies and risks
- "Do the thing now" culture for Sev1: urgent fixes are prioritized (admin merges, hotfix branches) but the repo often skips the full GitHub incident workflow and postmortem closure, reducing long-term traceability (PR #213, ops/incidents.md notes).
- Metadata drift: multiple label conventions and severity formats make automated triage and filters brittle (`.github/LABELS.md`, ops/oncall.md).
- Unclear sign-off for breaking changes: `docs/api_versioning.md` admits the authority for approving breaking changes is not defined, yet PR #220 proceeds with a new major API surface.
- Oncall expectations vs reality: `ops/oncall.md` prescribes SLAs and issue creation, but the incident log and PR notes show Slack-first escalations and missing postmortems.

## What a new backend engineer or SRE must know ✅
- Expect urgency: Sev1s are often fixed by hotfix branches and fast merges (see PRs #213 and #215); be prepared to coordinate in Slack and with oncall immediately.
- Don't assume perfect metadata: check labels manually (the repo mixes `sev1` / `sev-1` / `priority-high`) and prefer confirming severity in the issue text or incidents log.
- Follow the intended process but capture the trail: open or link an `incident`-labeled issue for outages, add the follow-up notes to `ops/incidents.md`, and link hotfix PRs to incident issues when possible (the repo intends this, see `CONTRIBUTING.md` and ops/incidents.md).
- For breaking API/DB/infra proposals: document changes in `docs/api_versioning.md` / RELEASE_NOTES and call out who you expect to approve them — the repo currently lacks a single clear approver and treats some decisions informally (see PR #220 and docs/api_versioning.md).

## Short recommendations for onboarding (practical)
- When responding to an incident, create a GitHub incident issue even if you coordinate in Slack; link hotfix PRs to that issue so the timeline is preserved (ops/incidents.md shows missing Slack history).
- When labeling, use the newer `area:*` and `sev*` forms if possible; watch for legacy variants documented in `.github/LABELS.md`.


---
Report generated from repository files: `CONTRIBUTING.md`, `.github/LABELS.md`, `.github/PULL_REQUESTS.md`, `.github/MILESTONES.md`, `docs/api_versioning.md`, `ops/incidents.md`, and `ops/oncall.md` (examples and incidents cited above).