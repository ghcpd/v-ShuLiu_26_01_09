# Meta Analysis Report — Collaboration & Operations

**Scope:** Review of contribution and ops artifacts to infer how backend work and incidents are coordinated in practice.

---

## Executive summary ✅

- Documentation expresses clear intentions (branching, labels, reviews, incident follow-up) in `CONTRIBUTING.md`, `.github/*` and `docs/api_versioning.md`.
- In practice, several shortcuts and ad-hoc decisions appear repeatedly (merge overrides, inconsistent labels, Slack-first escalation) as evidenced by Issues #101–#108 and PRs #210, #213, #215, #220, #221.
- Key risk areas: incident postmortems not consistently captured, breaking-change approval unclear, labeling inconsistent, and rollback policies incomplete.

---

## Evidence & observed patterns (by topic) 🔎

### Incidents & hotfixes

- Intended: `CONTRIBUTING.md` requires an `incident`-labeled follow-up issue for Sev1 incidents and a post-incident review in `ops/incidents.md`.
- Actual behavior: Several Sev1 incidents were handled with ad-hoc fixes and partial documentation:
  - Issue #101 (GET /todos 500s) links the production outage to PR #210; fix landed in PR #213 and a retrospective note exists, but the incident entry says "Some discussion happened in Slack and was not fully copied here" (`ops/incidents.md`).
  - Issue #102 (worker stalls) used label `sev-1` (hyphenated) and lacked an initial formal postmortem; fix in PR #215 but postmortem is informal (weekly notes) per `ops/incidents.md`.
- Hotfix practice: PR #213 description and `.github/PULL_REQUESTS.md` notes show hotfixes were sometimes merged directly to `main`, even with CI failing, via overrides ("Merging this directly to main with admin override; tests are flaky").

### Breaking API / DB / infra changes

- Intended: `docs/api_versioning.md` prescribes new versioned paths for breaking changes and a deprecation window (discussed as "6 months").
- Actual behavior: Breaking changes get merged while discussions about deprecation windows / authority to approve remain unresolved.
  - PR #220 introduces `/v2/todos` while the doc notes "it's unclear who has final authority to approve a breaking change".
  - PR #210 (DB/ORM bump) triggered production failures (Issue #101) and PR #213 was used as a quick fix; no explicit canary/rollout process is documented or followed consistently (see PR #210 notes in `.github/PULL_REQUESTS.md`).

### Ownership & responsibilities (backend vs SRE/platform)

- Intended: `CONTRIBUTING.md` expects backend changes reviewed by `@backend-core`, infra by `@sre`/`@platform`, and oncall SREs to be available for infra issues.
- Actual: Responsibilities blur during incidents.
  - Oncalls often make rapid decisions (manual rollbacks, hotfix merges) without a consistent follow-up, and comments show that "whomever is oncall decides during incidents" (Issue #105 discussion summarized in `.github/ISSUES.md`).
  - SREs sometimes merge urgent fixes (PR #213 and PR #215 show SRE/maintainer-led fast merges).

### Labeling and metadata inconsistencies

- `.github/LABELS.md` explicitly notes mixed conventions (e.g., `bug` vs `type:bug`, `sev1` vs `sev-1`, `infra` vs `area:infra`).
- Issues demonstrate this: Issue #101 used `sev1`, Issue #102 used `sev-1`, and Issue #104 specifically calls out label focus.
- Some status labels (`in-progress`, `blocked`, `needs-triage`) are used irregularly.

---

## Key inconsistencies between docs and practice ⚠️

- Incident recording: Docs require a post-incident entry in `ops/incidents.md` and an `incident`-labeled issue; in practice some incidents were handled in Slack with only partial GitHub records (Issue #101, `ops/incidents.md` comment: "Some discussion happened in Slack and was not fully copied here").
- Hotfix merging: Policy expects PRs to pass CI and receive approvals, but PR #213 was merged via override despite flaky tests.
- Breaking-change authority: `docs/api_versioning.md` flags this as an open question; PR discussions (PR #220) show the team proceeds before a formal decision is recorded.
- Labeling: `CONTRIBUTING.md` asks for `sev1/2/3` but real usage includes `sev-1` and `priority-high` (see `ops/oncall.md`, Issue #102, Issue #104).

---

## What a new backend engineer or SRE should know 🧭

- Incident response:
  - Expect rapid, pragmatic action oncall (manual rollbacks, admin merges). See Incident examples: Issue #101 (PR #210 → PR #213) and Issue #102 (PR #215).
  - Follow-up is expected but not guaranteed—check `ops/incidents.md` and search Slack/channel history for context. Proactively create an `incident`-labeled issue when you act as oncall.
- Hotfixes & CI:
  - Admin overrides happen in practice; still, prefer to document the reason and add a follow-up issue or comment (PR #213 notes show this was not consistently done).
- Breaking changes:
  - Treat API/DB changes as high-risk: link PRs to issues, document deprecation windows in `docs/api_versioning.md`, and call out reviewers (backend-core + SRE/platform). Expect discussion about canarying and rollout (see PR #210 discussion).
- Labels and triage:
  - Don't assume consistent label usage—check for both `sev1` and `sev-1`, `bug` and `type:bug`. If adding labels, prefer the `area:*` and `sev*` conventions in `CONTRIBUTING.md` and `.github/LABELS.md`.
- Where to look for authoritative info:
  - Primary docs: `CONTRIBUTING.md`, `ops/oncall.md`, `ops/incidents.md`, `docs/api_versioning.md`, and `.github/*` files. But be prepared for divergence between docs and practice; PR comments and issue threads often contain the de facto decisions (see `.github/PULL_REQUESTS.md` archive).

---

## Recommendations (short, doc-focused) 💡

- Formalize the decision path for breaking changes and encode who approves them (backend lead / product / architecture review). Evidence: `docs/api_versioning.md` notes this gap; PR #220 discussion.
- Normalize labels by choosing a canonical scheme (`area:*`, `type:bug`, `sev1`) and retroactively cleaning high-traffic issues (Issue #108 references this need).
- Make incident postmortems mandatory for Sev1 and track completion of action items in `ops/incidents.md` (Issue #101 and `ops/incidents.md` show partial follow-up).

---

## Files & items cited (quick reference) 📚

- `CONTRIBUTING.md` (branching, labels, incident expectations)
- `.github/LABELS.md`, `.github/ISSUES.md`, `.github/PULL_REQUESTS.md` (examples, label/state usage)
- `ops/incidents.md`, `ops/oncall.md` (incident log, oncall reality)
- `docs/api_versioning.md` (rules for breaking changes)
- Issues & PRs noted in examples: Issue #101, #102, #103, #104, #105, #108; PR #210, #213, #215, #220, #221.

---

*Report generated by an automated repository review. If you'd like, I can open a small issues/PR to codify one of the short recommendations (e.g., canonical label doc or a breaking-change decision ADR).* 
