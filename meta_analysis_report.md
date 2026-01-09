# Meta-Analysis Report: Collaboration and Operations Patterns

**Repository:** Todo API Service (Python/FastAPI)  
**Analysis Date:** January 9, 2026

---

## Executive Summary

This repository shows evidence of an evolving open-source project that has grown from a small team to a multi-contributor effort involving backend engineers and SREs. While written guidelines exist, actual operational practices have diverged in key areas. This report synthesizes evidence from CONTRIBUTING.md, docs/, ops/, .github metadata, and synthetic issue/PR archives to identify collaboration patterns, inconsistencies, and practical knowledge new contributors need.

---

## 1. Collaboration & Governance Patterns

### 1.1 Intended Workflow

[CONTRIBUTING.md](CONTRIBUTING.md) defines the following **intended** process:

- **Branching:** Feature branches (`feat/`), bugfix (`fix/`), hotfix (`hotfix/<incident-id>`)
- **PR Requirements:** Target `main`, link to issues, require one approval from `@backend-core`, pass CI
- **Issue Labeling:** Use area labels (`area:api`, `area:db`, `area:infra`) and severity labels (`sev1`, `sev2`, `sev3`)
- **Incident Handling:** Sev1 incidents must have follow-up issues labeled `incident` and `sev1`, with post-incident reviews added to [ops/incidents.md](ops/incidents.md)

### 1.2 Observed Reality

Evidence from [.github/ISSUES.md](.github/ISSUES.md), [.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md), [.github/LABELS.md](.github/LABELS.md), [ops/incidents.md](ops/incidents.md), and [ops/oncall.md](ops/oncall.md) reveals **significant divergence**:

**Label Inconsistencies:**
- Multiple severity schemes coexist: `sev1`, `sev-1`, `priority-high` (see Issue #102, Issue #104, [.github/LABELS.md](.github/LABELS.md))
- Bug labels vary: `bug`, `type:bug`, `defect`
- Area labels overlap: `backend` (old) vs. `area:api`/`area:db` (new)
- Issue #108 explicitly calls out this inconsistency as a meta-problem

**Incident Handling Gaps:**
- **Issue #101** (Sev1 outage from PR #210): Post-incident review was added as GitHub comments, not formally recorded in [ops/incidents.md](ops/incidents.md)
- **Issue #102** (Background worker stalls): Marked `sev-1` (hyphenated), oncall escalation happened in Slack without GitHub trail, and no formal postmortem was written despite [ops/oncall.md](ops/oncall.md) stating postmortems must occur within 3 business days
- **PR #213** (hotfix): Merged with CI failures via admin override; no documented exception policy

**Authority Ambiguity:**
- **Issue #105**: Contributors openly ask "Who approves schema changes?" Answer given informally ("whomever is oncall during incidents, backend-core for planned work") but never documented
- [docs/api_versioning.md](docs/api_versioning.md) explicitly notes: "It's unclear who has final authority to approve a breaking change"
- **PR #220** discussion references an "API versioning ADR" and informal architecture review decisions, but these are not linked or discoverable

---

## 2. Ownership & Responsibility Distribution

### 2.1 Backend vs. SRE Roles

[CONTRIBUTING.md](CONTRIBUTING.md) states:
- Backend changes: reviewed by `@backend-core`
- Deployment/infra changes: reviewed by `@sre` or `@platform`

[ops/oncall.md](ops/oncall.md) describes:
- Weekly oncall rotation among backend engineers
- SREs provide backup for infrastructure-related issues

### 2.2 Observed Patterns

**Incident Ownership:**
- **Issue #101**: Oncall SRE performed manual rollback in Kubernetes, but did not revert DB migration because "we usually don't roll back DB migrations unless strictly necessary" (no written policy)
- [ops/incidents.md](ops/incidents.md) notes for Issue #101: Some discussion happened in Slack and was not fully copied into GitHub

**Deployment Decisions:**
- **PR #210** discussion: Reviewer suggested canary deployment, maintainer responded "We don't really have a documented canary process yet"
- [docs/architecture.md](docs/architecture.md) states deployments "should" go through staging before production, but PR #213 (hotfix) was merged directly to main with partial CI failures

**Practical Reality:**
- In time-sensitive incidents, ad-hoc decisions are made by whomever is oncall
- Backend engineers and SREs coordinate informally in Slack
- Written policies exist but are overridden when necessary, without consistent documentation of exceptions

---

## 3. Breaking Changes & Approval Process

### 3.1 Documented Guidelines

[docs/api_versioning.md](docs/api_versioning.md) describes **intended** approach:
- Avoid breaking changes whenever possible
- When necessary, introduce versioned paths (e.g., `/v2/todos`)
- Maintain old versions for at least one deprecation window (informally discussed as "6 months")

### 3.2 Observed Gaps

**Authority Ambiguity:**
- [docs/api_versioning.md](docs/api_versioning.md) explicitly states: "It's unclear who has final authority to approve a breaking change: Backend lead? Product owner? Architecture review group?"

**Inconsistent Application:**
- **PR #220** (introducing `/v2/todos`): Labeled `api-breaking`, discussion mentions an informal 6-month deprecation window and an "architecture review", but no formal approval documented
- Author notes: "API versioning ADR is still in draft; let's merge and update docs later"
- **Issue #103** (soft-delete feature): Debate over whether this is a breaking change requiring versioning, with references to an "API versioning ADR" that is not easily discoverable

**Database Migrations:**
- **Issue #105**: Asks "Who approves schema changes?" 
- Response: "In practice, whomever is oncall decides during incidents" and "For planned work, backend-core leads, but I don't see it documented"
- Issue closed after brief answer, no documentation update made

---

## 4. Incident & Hotfix Handling

### 4.1 Written Expectations

[CONTRIBUTING.md](CONTRIBUTING.md) and [ops/oncall.md](ops/oncall.md) state:
- Sev1 incidents must have follow-up issue labeled `incident` and `sev1`
- Oncall must respond within 15 minutes
- Post-incident review scheduled within 3 business days
- Review added to [ops/incidents.md](ops/incidents.md)

### 4.2 Actual Practice

**Issue #101** (2024-10-01 outage):
- Hotfix PR #213 merged directly to `main` with CI failing
- Admin override used: "tests are flaky and we don't have time to stabilize them now"
- Maintainer comment: "We should document this kind of exception somewhere (incident playbook?)"
- Post-incident notes scattered between GitHub comments and [ops/incidents.md](ops/incidents.md)

**Issue #102** (2024-11-12 worker stalls):
- Labeled `sev-1` instead of `sev1`
- [ops/incidents.md](ops/incidents.md) notes: "No dedicated postmortem entry was added initially; notes were mentioned in a weekly ops sync"
- Follow-up PR #215: Backend lead says "Let's just reference this PR in the weekly ops sync notes" instead of formal incident issue

**Rollback Policies:**
- **Issue #101**: SRE rolled back application deployment but not DB migration
- [ops/incidents.md](ops/incidents.md) action item: "Document rollback policies for DB migrations" — marked as "Partially addressed, not formally closed"

---

## 5. Key Inconsistencies Between Documentation and Behavior

| **Area** | **Documentation Says** | **Reality Shows** | **Evidence** |
|----------|------------------------|-------------------|--------------|
| **Severity Labels** | Use `sev1`, `sev2`, `sev3` | Mix of `sev1`, `sev-1`, `priority-high` | Issue #102, Issue #104, [.github/LABELS.md](.github/LABELS.md) |
| **Incident Postmortems** | All Sev1 incidents get formal review in [ops/incidents.md](ops/incidents.md) | Some incidents documented only in PR comments or Slack | Issue #101, Issue #102, [ops/incidents.md](ops/incidents.md) |
| **Breaking Change Approval** | Follow [docs/api_versioning.md](docs/api_versioning.md) | No clear approval authority; decisions made informally | Issue #103, Issue #105, PR #220, [docs/api_versioning.md](docs/api_versioning.md) |
| **CI/Test Requirements** | All PRs must pass CI before merge | Hotfixes merged with admin override despite failing tests | PR #213 |
| **Deployment Process** | Go through staging first | Hotfixes deploy directly to production | PR #213, [docs/architecture.md](docs/architecture.md) |
| **DB Migration Rollback** | Should document rollback policies | No written policy; oncall decides case-by-case | Issue #101, [ops/incidents.md](ops/incidents.md) |
| **Escalation Process** | Oncall opens incident issue with proper labels | Escalation often happens in Slack without GitHub trail | Issue #102, [ops/oncall.md](ops/oncall.md) |

---

## 6. What New Contributors Need to Know

### 6.1 For Backend Engineers

**Formal Guidelines Exist But Are Not Strictly Enforced:**
- Read [CONTRIBUTING.md](CONTRIBUTING.md), [docs/api_versioning.md](docs/api_versioning.md), and [docs/architecture.md](docs/architecture.md) for baseline expectations
- Be aware that during incidents, these guidelines are sometimes overridden (e.g., PR #213 merged with failing CI)

**Breaking Changes Are Ambiguous:**
- [docs/api_versioning.md](docs/api_versioning.md) is still a draft and lacks clear approval authority
- If proposing a breaking API or DB change, expect debate (see Issue #103, Issue #105)
- Look for informal precedents in PR discussions (e.g., PR #220)

**Label Usage Is Inconsistent:**
- Prefer newer conventions: `area:api`, `area:db`, `area:infra`, `sev1` (without hyphen)
- Expect to see older labels like `backend`, `bug`, `priority-high` in existing issues
- Issue #108 proposes label normalization but is still open

### 6.2 For SREs / Platform Engineers

**Oncall Responsibilities Are Partially Documented:**
- [ops/oncall.md](ops/oncall.md) describes expectations (15-minute response, open incident issues, schedule postmortems)
- Reality: Some incidents (Issue #102) skip formal postmortems; escalation happens in Slack

**Rollback Policies Are Informal:**
- DB migrations are generally not rolled back (per Issue #101 discussion)
- Application deployments can be rolled back via Kubernetes, but this is not formally documented
- [ops/incidents.md](ops/incidents.md) action item to document rollback policies is still open

**Deployment Process Lacks Formal Canary / Staging Policy:**
- [docs/architecture.md](docs/architecture.md) says deployments "should" go through staging
- **PR #210** discussion shows maintainers acknowledge lack of canary process
- Hotfixes (PR #213) bypass staging entirely

### 6.3 General Observations

**Slack vs. GitHub:**
- Important decisions and escalations often happen in Slack and are not consistently copied to GitHub
- Example: Issue #101 and Issue #102 both mention "discussion happened in Slack"

**Documentation Lags Behind Practice:**
- **PR #221** (open): Attempts to align [ops/incidents.md](ops/incidents.md) with actual oncall behavior
- Reviewer notes: "This reflects what we did in the last few incidents, but differs from CONTRIBUTING.md. We need a decision on which is source of truth."

**Incident Handling Prioritizes Speed Over Process:**
- Admin overrides and CI bypasses are used during Sev1 incidents (PR #213)
- Postmortems and documentation updates are often deferred or forgotten

---

## 7. Recommendations for Aligning Practice and Documentation

1. **Label Normalization (Issue #108):**
   - Complete the effort to standardize on `sev1`/`sev2`/`sev3`, `area:*`, and `type:*` labels
   - Update [.github/LABELS.md](.github/LABELS.md) as the canonical reference
   - Create a script or workflow to flag non-standard labels

2. **Clarify Authority for Breaking Changes:**
   - Finalize the "API versioning ADR" referenced in Issue #103 and PR #220
   - Document in [docs/api_versioning.md](docs/api_versioning.md) who has final approval for API and DB schema changes
   - Link from [CONTRIBUTING.md](CONTRIBUTING.md) to this decision

3. **Formalize Incident Postmortem Process:**
   - Update [ops/oncall.md](ops/oncall.md) to reflect actual practice (or enforce documented practice)
   - Require all Sev1 incidents to have a GitHub issue + entry in [ops/incidents.md](ops/incidents.md)
   - Close the action item from Issue #101: Document DB migration rollback policies

4. **Document Exception Policies:**
   - Create an "incident playbook" section in [ops/incidents.md](ops/incidents.md) or [CONTRIBUTING.md](CONTRIBUTING.md) covering:
     - When admin CI overrides are acceptable (PR #213)
     - How to escalate for approvals outside normal review channels
     - How to retroactively document decisions made in Slack

5. **Reconcile [CONTRIBUTING.md](CONTRIBUTING.md) and Actual Workflows:**
   - Review open PR #221 and decide whether [CONTRIBUTING.md](CONTRIBUTING.md) or [ops/incidents.md](ops/incidents.md) is source of truth
   - Update whichever is chosen to reflect reality

6. **Add Deployment and Canary Policies:**
   - Document (or create) a canary/staging process in [docs/architecture.md](docs/architecture.md)
   - Clarify when bypassing staging is acceptable (e.g., only for Sev1 hotfixes with explicit approval)

---

## 8. Conclusion

The Todo API Service repository demonstrates a common pattern in growing open-source projects: **documentation established early is overtaken by pragmatic, informal practices as the team scales**. The written guidelines in [CONTRIBUTING.md](CONTRIBUTING.md), [docs/api_versioning.md](docs/api_versioning.md), and [ops/incidents.md](ops/incidents.md) represent aspirational best practices, but actual collaboration relies heavily on Slack discussions, ad-hoc oncall decisions, and informal precedents visible only in issue/PR threads.

Key areas of divergence:
- **Label inconsistency** (Issue #104, Issue #108, [.github/LABELS.md](.github/LABELS.md))
- **Incident postmortem gaps** (Issue #101, Issue #102)
- **Unclear authority** for breaking changes (Issue #103, Issue #105, [docs/api_versioning.md](docs/api_versioning.md))
- **Hotfix process bypasses** documented requirements (PR #213, PR #215)

New contributors—both backend engineers and SREs—should:
- Treat documentation as a starting point, not absolute truth
- Expect to learn operational norms from PR discussions and oncall handoffs
- Advocate for reconciling documentation with practice where discrepancies cause confusion

Maintainers should prioritize closing the gap between written policy and lived experience to reduce onboarding friction and improve operational consistency.

---

**Generated:** January 9, 2026  
**Based on:** CONTRIBUTING.md, docs/api_versioning.md, docs/architecture.md, ops/incidents.md, ops/oncall.md, .github/ISSUES.md, .github/PULL_REQUESTS.md, .github/LABELS.md, .github/MILESTONES.md, README.md
