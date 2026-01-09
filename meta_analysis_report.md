# Collaboration & Operations Meta-Analysis: Todo API Service

## Executive Summary

The Todo API Service exhibits a common pattern in growing open-source projects: **documented processes exist but practical coordination happens through ephemeral channels (Slack, oncall notes, PR comments).** While CONTRIBUTING.md, docs/api_versioning.md, and ops/ define intended workflows, actual decisions on incidents, breaking changes, and role responsibilities remain inconsistent. New contributors would struggle to understand authority structures and exception handling.

---

## Main Collaboration & Governance Patterns

### 1. Incident Response: Documented Intent vs. Informal Reality

**Documented process** (CONTRIBUTING.md, oncall.md):
- Sev1 incidents must spawn a labeled GitHub issue with `incident` and `sev1` tags
- A post-incident review must be recorded in ops/incidents.md within 3 business days

**Actual behavior** (evidence from ops/incidents.md and issue archive):

- **Issue #101** (Sev1: `GET /todos` 500 errors): 
  - Incident occurred after PR #210 merged
  - Oncall SRE applied manual rollback in Kubernetes but **did not revert the DB migration**
  - A GitHub issue was filed retroactively, not immediately
  - Post-incident review added only as comments, not formally recorded in ops/incidents.md
  - Rollback policy for DB migrations remains undocumented

- **Issue #102** (Sev1: Background worker stalls):
  - Severity label inconsistency: used `sev-1` instead of `sev1`
  - Escalation happened in Slack; no consistent GitHub trail
  - No formal postmortem added to ops/incidents.md initially
  - Comment states: "we'll add this to the next incident review batch" (status unclear)

**Gap:** Severity labeling itself is inconsistent (sev1 vs. sev-1 vs. priority-high), making aggregation and reporting difficult. Issue #104 is open requesting clarification but unresolved.

### 2. Breaking API & Schema Changes: Unclear Authority

**Documented process** (docs/api_versioning.md):
- Avoid breaking changes; use versioned paths like `/v2/todos`
- Maintain old versions for ≥6 months
- Changes must be documented in API docs and RELEASE_NOTES

**Key ambiguities in documented process:**
- **6-month deprecation window is informal, not formally agreed** per the draft itself
- **Who approves breaking changes is undefined:** "It's unclear who has final authority to approve a breaking change: Backend lead? Product owner? Architecture review group?"

**Actual behavior** (evidence from issues and PRs):

- **Issue #103** (Soft-delete feature):
  - Disagreement on whether soft-delete semantics constitute a breaking change
  - References an "API versioning ADR" that is not discoverable or linked
  - No resolution recorded; decision deferred

- **Issue #105** (Who approves schema changes?):
  - One maintainer: "In practice, whomever is oncall decides during incidents"
  - Another: "For planned work, backend-core leads, but I don't see it documented"
  - Issue closed without updating governing docs

- **PR #220** (Introduce `/v2/todos`):
  - Author acknowledges: "We agreed in the last architecture review to maintain both for 6 months, but I don't see it written down"
  - API versioning ADR is still in draft; merge deferred pending doc updates
  - Shows real decision-making happens in meetings/discussions, not recorded systematically

**Gap:** Planned breaking changes rely on informal decisions and architecture review meetings. During incidents, authority defaults to whoever is oncall at the time. No SLA or escalation chain is documented.

### 3. Backend vs. SRE/Platform Role Boundaries

**Documented process** (CONTRIBUTING.md):
- Backend changes reviewed by `@backend-core`
- Deployment/infra changes reviewed by `@sre` or `@platform`

**Actual behavior** (evidence from PR patterns and incidents):

- **PR #210** (Connection pooling & ORM bump):
  - Backend-heavy change with infrastructure implications
  - PR discussion shows: SRE asked to coordinate with oncall, but no formal handoff process
  - Post-merge, this PR triggered Issue #101; no explicit incident → PR linking

- **PR #213** (DB timeout hotfix):
  - Oncall SRE: "Merging directly to main with admin override; tests are flaky and we don't have time"
  - Shows incident urgency bypasses normal review gates
  - Comment: "We should document this kind of exception somewhere (incident playbook?)"
  - **No incident playbook exists**

- **PR #215** (Background worker stale task fix):
  - Merged to `hotfix/worker-stall` branch (hotfix branching convention in CONTRIBUTING.md)
  - SRE question: "Do we need a formal incident here?" — no clear answer
  - Backend lead deferred to "weekly ops sync notes" (informal, not on GitHub)

**Gap:** Boundary between backend-core and SRE/platform is fluid. Under incident pressure, SREs can merge code directly with admin override. Incident decision-making (severity assessment, escalation, post-mortems) happens offline and is not captured in GitHub consistently.

### 4. Label Ecosystem: Multiple Overlapping Conventions

**Evidence** (.github/LABELS.md):

- **Severity labels:** `sev1`, `sev2`, `sev3` (intended) vs. `sev-1`, `priority-high` (actual usage)
- **Bug-type labels:** `bug`, `type:bug`, `defect` (three separate labels)
- **Area labels:** `backend`, `area:api`, `area:db`, `area:infra`, `infra` (five overlapping conventions)
- **Process labels:** `in-progress`, `blocked`, `needs-triage` — introduced recently but applied inconsistently
- **Help wanted:** `good first issue` vs. `good-first-issue` (hyphenation inconsistency)

**CONTRIBUTING.md acknowledges this:**
> In practice, some older issues use different label schemes (e.g., `type:bug`, `defect`, `priority-high`). We are **gradually normalizing** labels.

**Gap:** No runnable process to migrate/normalize labels. Issue #108 (Meta: Align label usage) remains open, indicating this is a known problem without a resolution path.

---

## Key Inconsistencies: Documented vs. Actual Behavior

| Process | Documented | Actual | Evidence |
|---------|-----------|--------|----------|
| **Incident labeling** | Issue must be tagged with `incident` + `sev1/2/3` | Labels use `sev-1`, `priority-high` inconsistently | Issues #101, #102, #104 |
| **Incident postmortems** | Must be recorded in ops/incidents.md within 3 business days | Reviews added as PR comments or deferred to "next batch" | Issue #102, PR #221 |
| **DB migration rollbacks** | Unclear (not documented) | "Usually don't roll back unless strictly necessary" (informal policy in PR comments) | Issue #101 discussion |
| **Breaking change approval** | Unclear (doc says ambiguous) | Approval authority defaults to whoever is oncall during incidents; planned changes discussed in architecture reviews (not recorded) | Issues #103, #105, PR #220 |
| **SRE vs. Backend review** | SRE reviews infra/deployment; Backend-core reviews backend | SREs can merge with admin override under incident pressure | PR #213 |
| **Hotfix branching** | Convention defined in CONTRIBUTING.md: `hotfix/<incident-id>` | Hotfix branches are used but incident linkage unclear | PR #215 uses `hotfix/worker-stall` |
| **Feature vs. incident tracking** | Incidents get `incident` label; features are separate | Boundary blurred; PR #215 asks "Do we need a formal incident here?" | PR #215 discussion |
| **Canary deployment** | Not documented | PR #210 discussion shows no formal canary process exists; instead, "just monitor logs after deploy" | PR #210 discussion |

---

## Gaps Requiring New Documentation or Process

### 1. **Incident Playbook**
Currently missing. Should define:
- Severity criteria (what qualifies as Sev1 vs. Sev2?)
- Escalation chain and oncall authority limits
- Exception procedures (e.g., when can oncall merge without full CI/review?)
- Postmortem template and 3-business-day SLA enforcement

*Evidence:* PR #213 comment explicitly requests this.

### 2. **DB Migration Rollback Policy**
Currently implicit ("usually don't roll back unless necessary"). Should document:
- When migrations can be rolled back
- When they cannot (and why)
- Coordination between backend and SRE/platform during incidents

*Evidence:* Issue #101 discussion shows ad-hoc decisions.

### 3. **Architecture Decision Records (ADRs)**
Currently referenced but not discoverable. Should include:
- API versioning decision (6-month deprecation window, authority to approve)
- Multi-tenant schema strategy
- Deployment cadence and canary policy
- Role boundaries between backend-core and SRE/platform

*Evidence:* Issues #103, #105, and PR #220 all reference decisions not in GitHub.

### 4. **Label Normalization Runbook**
Issue #108 is open; no runbook exists. Should specify:
- Target label schema (which takes precedence: `sev1` or `sev-1`?)
- Migration path for existing issues
- Automation/bot rules to prevent new inconsistencies

*Evidence:* .github/LABELS.md acknowledges "gradual normalization" but shows no automation or migration plan.

### 5. **Breaking Change Approval Process**
Currently undefined. Should clarify:
- Who decides: backend lead, product, or architecture committee?
- How is decision documented?
- What triggers a formal architecture review vs. a PR discussion?

*Evidence:* Issue #105 shows disagreement; PR #220 shows decision happens outside GitHub.

---

## What New Backend Engineers & SREs Must Learn

### For Backend Engineers
1. **Incident decision-making is offline.** Watch Slack and weekly ops sync notes, not just GitHub issues. If you're oncall and have to merge a hotfix with CI failures, document the exception in the PR.
2. **Breaking API changes are discussed in architecture reviews** (timing and attendees TBD; ask your tech lead). Referencing "the ADR" will not work—ask for specifics.
3. **Label your issues carefully,** but know that old issues use different label schemes. When filtering by severity, check for both `sev1` and `sev-1`.
4. **Tests can be overridden under incident pressure,** but expect a follow-up to document the decision and stabilize tests later (e.g., PR #213 → test stability in v1.3.0 milestone).

### For SREs/Platform
1. **You have authority to merge urgent fixes during incidents,** but this should be recorded (e.g., in the incident issue and ops/incidents.md) so the team can learn.
2. **DB migrations are sticky.** If a backend change includes a migration, coordinate rollback policy upfront. Document whether you can safely roll back without data loss.
3. **Incident postmortems are expected in ops/incidents.md,** but in practice, they sometimes get added late or deferred. Push back on deferment; create a GitHub issue to track it (e.g., "postmortem for incident X").
4. **Watch for architecture review decisions mentioned in PRs and issue comments.** These are often the ground truth, even if not in a discoverable doc.

### For All Contributors
1. **Reference everything on GitHub.** Slack discussions are ephemeral. If a decision is made in a meeting or Slack thread, open an issue or PR comment to capture it.
2. **Expect label inconsistency,** but try to use the newer `area:*` and `sev1/2/3` conventions when opening new issues.
3. **Deployment, canary, and rollback processes are underdocumented.** Ask oncall or a tech lead before assuming how to deploy safely.

---

## Summary Table: What Works, What Doesn't

| Aspect | Status | Why |
|--------|--------|-----|
| **Code review gates** | ✅ Works (mostly) | CI checks and `@backend-core` approval enforced for normal PRs |
| **Incident response** | ⚠️ Partial | Fast reactions happen; formal documentation lags. Severity labeling inconsistent. |
| **Breaking change governance** | ❌ Doesn't work | Authority undefined; decisions happen in meetings, not systematically recorded |
| **Role clarity (backend vs. SRE)** | ⚠️ Partial | Clear in normal work; collapses under pressure. SREs can override gates in emergencies. |
| **Label hygiene** | ❌ Doesn't work | Multiple overlapping conventions; "gradual normalization" in progress but unmeasured. |
| **Postmortem tracking** | ❌ Doesn't work | ops/incidents.md is intended log but in practice is incomplete. Decisions to defer updates to "next batch." |
| **API versioning** | ⚠️ Partial | Strategy documented (v1 vs. v2); approval process and deprecation SLA are not. |

---

## Conclusion

This repository demonstrates effective **tactical incident response** (fast rollbacks, oncall engagement) but weak **strategic governance** (no ADRs, broken label system, role ambiguity). The team acknowledges gaps (Issues #104, #105, #108 are open) but has not yet systematized their resolution.

**To unblock growth and reduce friction:**
1. Publish the API versioning ADR and architecture decision-making process
2. Create and enforce an incident playbook with postmortem SLAs
3. Automate label migration and establish a policy for future consistency
4. Document role boundaries and incident escalation explicitly

Until these are addressed, knowledge resides in oncall handoff notes, weekly syncs, and PR comments—not in searchable, version-controlled documentation.
