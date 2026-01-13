# Meta-analysis: collaboration & ops patterns — Todo API service

Summary
- Concise finding: the repository has clear, pragmatic docs for incidents, hotfixes, and API versioning, but practice frequently diverges under time pressure (label drift, skipped postmortems, ad-hoc hotfix merges). Evidence is documented below with concrete examples. ✅

## 1) Quick orientation (for a new backend engineer or SRE)
- Read first: `CONTRIBUTING.md`, `ops/oncall.md`, `ops/incidents.md`, `docs/api_versioning.md`. 📚
- Triage essentials: open an `incident` issue and add a severity label (`sev1` preferred). (See `ops/oncall.md` and `CONTRIBUTING.md`.)
- Hotfix pattern you will see: branch `hotfix/<incident-id>`; oncall maintainers sometimes merge directly to `main` during outages (examples: PRs summarized in `.github/PULL_REQUESTS.md`). ⚠️

## 2) Main collaboration & governance patterns (observed)
- Formal documents exist and are reasonably comprehensive: `CONTRIBUTING.md` (hotfix branches, labels), `docs/api_versioning.md` (versioning rules), and `ops/oncall.md` / `ops/incidents.md` (incident expectations).
  - Evidence: `CONTRIBUTING.md` (hotfix workflow, required `sev1` for Sev1), `docs/api_versioning.md` (versioning rules).
- Oncall SREs act as primary responders and have operational latitude during incidents (investigate, rollback, merge hotfixes).
  - Evidence: `ops/oncall.md` (oncall responsibilities); `ops/incidents.md` (2024-10-01 timeline shows oncall SRE actions); `.github/PULL_REQUESTS.md` (examples of oncall/admin merges).
- Community + SRE reviewers share review responsibilities, but final approver for breaking changes is ambiguous and often decided ad hoc.
  - Evidence: `docs/api_versioning.md` notes "It's unclear who has final authority"; discussion in `.github/PULL_REQUESTS.md` and `.github/ISSUES.md` shows debate about approval.

## 3) How incidents & hotfixes are actually handled (evidence-based)
- Intended flow: respond within 15 minutes, open an `incident` issue, tag with `sev1` + area labels, schedule post-incident review (`ops/oncall.md`, `CONTRIBUTING.md`).
- Observed deviations:
  - Label inconsistency: issues use `sev1`, `sev-1`, and `priority-high` interchangeably (see `ops/oncall.md`, `.github/ISSUES.md`, `.github/LABELS.md`). Example: Issue #102 uses `sev-1` while the incident log marks it `Sev1` (`ops/incidents.md` / `.github/ISSUES.md`).
  - Missing postmortems or informal follow-ups: several Sev1 incidents were resolved via PRs without a full postmortem in `ops/incidents.md` (see PR #213, PR #215 and notes in `.github/ISSUES.md`).
  - Hotfix fast-tracks: maintainers/oncall sometimes merge hotfixes with admin override and flaky tests (example discussion in `.github/PULL_REQUESTS.md`, PR summary for PR #210). This is accepted practice during outages but not uniformly documented.

## 4) How breaking API / DB / infra changes are proposed and approved
- Documented requirements: breaking API changes should be versioned (e.g., `/v2`) and recorded in `docs/api_versioning.md` and release notes; deployment/infra changes should be reviewed by SRE/platform (`CONTRIBUTING.md`).
  - Evidence: `docs/api_versioning.md`; `CONTRIBUTING.md` ("Deployment/infra changes: reviewed by @sre or @platform").
- Observed behavior & gaps:
  - Approval authority is ambiguous in practice — discussions defer to whoever is oncall or available during the decision window (`.github/ISSUES.md`, `.github/PULL_REQUESTS.md`).
  - ADRs and versioning guidance are drafty and sometimes ignored during merge (see discussion in `.github/PULL_REQUESTS.md` where an author says the "API versioning ADR is still in draft; let's merge and update docs later").
  - DB migrations during incidents can be partially rolled back (infra rollback without DB revert) — documented as a problem in `.github/ISSUES.md` (example note about a K8s rollback that didn't revert a DB migration).

## 5) Ownership & responsibility (backend vs SRE/platform)
- Stated split:
  - Backend: API implementation, feature behavior, maintaining API compatibility (`docs/api_versioning.md`, `CONTRIBUTING.md`).
  - SRE/Platform: deployment, runbook/oncall, infra changes, monitoring.
  - Evidence: `CONTRIBUTING.md`, `ops/oncall.md`.
- Practical overlap / handoff patterns:
  - Oncall SREs take operational decisions during incidents (including emergency merges/rollbacks). `.github/ISSUES.md` records that "whomever is oncall decides during incidents."
  - Platform review is expected for infra changes, but ad-hoc merges and ambiguous approval mean ownership often defaults to the person who’s available.

## 6) Key inconsistencies between docs and behavior (short list with evidence)
| Topic | Documented | Actual / observed | Example evidence |
|---|---:|---|---|
| Severity labels | `sev1`/`sev2`/`sev3` (`.github/LABELS.md`) | Mixed use: `sev-1`, `priority-high`, etc. | Issue #102; `.github/ISSUES.md`; `ops/oncall.md` notes label drift |
| Post-incident reviews | Postmortem in `ops/incidents.md` required | Some Sev1s lack formal postmortems; informal comments only | PR #213, PR #215; `.github/ISSUES.md` |
| Breaking-change approval | Must follow `docs/api_versioning.md` and obtain review | Approval authority unclear; merges sometimes precede ADRs | `.github/PULL_REQUESTS.md` discussion; `docs/api_versioning.md` notes |
| Emergency merges / testing | Tests required; normal review flow | Oncall/admin merges accepted during incidents (flaky tests bypassed) | `.github/PULL_REQUESTS.md` (PR #210 example) |

## 7) What a new backend engineer or SRE needs to know (practical checklist) 🔧
- Read (in order): `CONTRIBUTING.md`, `ops/oncall.md`, `ops/incidents.md`, `docs/api_versioning.md`. ✅
- Triage: open an `incident` issue, add `sev1`/`sev2`/`sev3` (prefer the `sevN` form), and tag `area:api|db|infra` as appropriate. (See `ops/oncall.md` and `.github/LABELS.md`.)
- Hotfixes: create `hotfix/<incident-id>` branches; expect oncall to fast-track merges during outages — follow up by adding a postmortem link to `ops/incidents.md`. (See `CONTRIBUTING.md`, `.github/PULL_REQUESTS.md`.)
- Breaking changes: assume you must get both backend and SRE/platform reviewers; if in doubt, open an ADR and link it to the PR. `docs/api_versioning.md` is the source for intended behavior but treat it as drafty — escalate to maintainers for final approval.
- Communication: escalate in the oncall channel (Slack) — many real-world decisions are coordinated there but not recorded in docs (`.github/ISSUES.md` notes missing public escalation paths).

## 8) Low-friction fixes the project can make (operational, not feature-level)
- Normalize severity labels (`sev1` preferred) and add a short labeling HOWTO in `CONTRIBUTING.md` (evidence: label drift across `ISSUES.md` / `LABELS.md`).
- Enforce (or automate) linking hotfix PRs to incident issues/postmortems so follow-ups are not lost (`.github/PULL_REQUESTS.md`, `ops/incidents.md` examples show gaps).
- Clarify who approves breaking DB/schema changes (product vs backend vs SRE) — capture this in `docs/api_versioning.md` or an ADR.

## 9) Bottom line (one-paragraph summary)
The repo has sensible, well-intended collaboration and oncall docs, and the team follows practical, pragmatic incident responses (oncall-led hotfixes, rapid rollbacks). However, label drift, missing postmortems, and unclear approval authority for breaking changes are recurring gaps — a new engineer should assume decisions will often be made by whoever is oncall and should proactively link incidents → hotfix PRs → postmortems. 🔎

---
Artifacts referenced (select): `CONTRIBUTING.md`, `ops/oncall.md`, `ops/incidents.md`, `docs/api_versioning.md`, `.github/LABELS.md`, `.github/PULL_REQUESTS.md`, `.github/ISSUES.md`, Issue #102, PR #210, PR #213, PR #215, PR #221.

(Report generated from repository artifacts; I can open a small PR that normalizes labels and adds a short "incident checklist" if you want.)