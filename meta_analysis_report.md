# Meta Analysis Report: Collaboration & Operations Patterns

## Executive Summary

This report analyzes the Todo API repository's collaboration and operations practices based on documented processes and actual behavior in issues, PRs, and operational artifacts. The analysis reveals significant gaps between intended guidelines and real practice, particularly around incident handling, breaking change approval, and label consistency.

## Key Findings

### 1. Incident & Hotfix Handling: Informal Under Pressure

**Documented Process:**
- [CONTRIBUTING.md](CONTRIBUTING.md) states Sev1 incidents "must" have a follow-up issue labeled `incident` and `sev1`
- [ops/oncall.md](ops/oncall.md) requires oncall to open incident issues within 15 minutes and schedule post-incident reviews within 3 business days
- [ops/incidents.md](ops/incidents.md) is intended to record major incidents

**Actual Behavior:**
- **Issue #101**: Filed retroactively after incident; post-incident review added informally in comments, not in [ops/incidents.md](ops/incidents.md) ([.github/ISSUES.md](.github/ISSUES.md))
- **Issue #102**: Used `sev-1` label instead of standard `sev1` ([.github/ISSUES.md](.github/ISSUES.md), [ops/incidents.md](ops/incidents.md))
- **PR #213** (hotfix): Merged with CI partially failing via admin override; discussion noted lack of documented exception process ([.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md))
- **PR #215**: No formal postmortem created; team decided to address "in the next incident review batch" ([.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md))

**Evidence of Process Breakdown:**
- [ops/incidents.md](ops/incidents.md): "Some discussion happened in Slack and was not fully copied here"
- [ops/oncall.md](ops/oncall.md): "Escalation often happens in Slack without a consistent GitHub trail"
- [ops/incidents.md](ops/incidents.md): Action items from incident 2024-10-01 noted as "Partially addressed, not formally closed"

**Implications:**
During high-pressure incidents, teams prioritize immediate fixes over process compliance. Rollback decisions, postmortem creation, and documentation updates are often deferred or skipped.

### 2. Breaking API/DB/Infra Changes: Ambiguous Authority

**Documented Process:**
- [CONTRIBUTING.md](CONTRIBUTING.md) states "Breaking API changes **must** be documented in [docs/api_versioning.md](docs/api_versioning.md)"
- [docs/api_versioning.md](docs/api_versioning.md) describes intended versioning approach but flags open questions about approval authority

**Actual Behavior:**
- **Issue #103** (soft-delete feature): Debate over whether change is breaking; reference to undiscoverable "API versioning ADR" ([.github/ISSUES.md](.github/ISSUES.md))
- **Issue #105** (schema change approval): Closed without documentation update; comments reveal informal rule: "whomever is oncall decides during incidents" vs. "backend-core leads for planned work" ([.github/ISSUES.md](.github/ISSUES.md))
- **PR #210** (ORM version bump, connection pooling): No documented canary process; maintainer says "let's just monitor logs after deploy" ([.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md))
- **PR #220** (introduce `/v2/todos`): Discussion reveals 6-month deprecation window "agreed in last architecture review" but not written down; "API versioning ADR is still in draft" ([.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md), [docs/api_versioning.md](docs/api_versioning.md))

**Evidence of Ambiguity:**
- [docs/api_versioning.md](docs/api_versioning.md): "It's unclear who has final authority to approve a breaking change: Backend lead? Product owner? Architecture review group?"
- [.github/ISSUES.md](.github/ISSUES.md), Issue #101: "we usually don't roll back DB migrations unless strictly necessary, but this is not codified in docs"

**Implications:**
Decision-making authority is unclear and context-dependent. Verbal agreements from architecture reviews or retros are not reliably captured in version-controlled documentation.

### 3. Ownership & Responsibility Distribution: Role Boundaries Blur

**Documented Expectations:**
- [CONTRIBUTING.md](CONTRIBUTING.md): Backend changes reviewed by `@backend-core`; deployment/infra changes reviewed by `@sre` or `@platform`
- [ops/oncall.md](ops/oncall.md): Weekly oncall rotation among backend engineers; SREs provide backup for infrastructure issues

**Actual Behavior:**
- **PR #210**: Backend PR affecting infrastructure; SRE comments "Please at least coordinate with oncall" but no formal approval gate enforced ([.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md))
- **PR #213** (hotfix): Oncall SRE merged hotfix with admin override, overriding backend review process ([.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md))
- **Issue #101**: SRE performed manual rollback in Kubernetes but did not revert DB migration; decision rationale not documented ([.github/ISSUES.md](.github/ISSUES.md))
- **Issue #105**: Question about who approves schema changes; answers reflect practice varies by context (incident vs. planned work) ([.github/ISSUES.md](.github/ISSUES.md))

**Evidence:**
- [ops/incidents.md](ops/incidents.md): "Oncall SRE investigated logs" and "Manual rollback of application deployment (DB migration not rolled back)"
- [.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md): Multiple instances of role boundaries being negotiated in PR comments rather than predefined

**Implications:**
During incidents, whoever is oncall effectively has override authority regardless of role. For planned work, review expectations are clearer but still negotiable.

### 4. Label & Metadata Inconsistency: Reporting Friction

**Documented Standards:**
- [CONTRIBUTING.md](CONTRIBUTING.md) specifies area labels (`area:api`, `area:db`, `area:infra`) and severity labels (`sev1`, `sev2`, `sev3`)
- Note acknowledges "some older issues use different label schemes" and labels are "gradually normalizing"

**Actual Usage:**
- **Severity labels**: Both `sev1` (Issue #101) and `sev-1` (Issue #102) used ([.github/ISSUES.md](.github/ISSUES.md), [ops/incidents.md](ops/incidents.md))
- **Bug labels**: Mix of `bug`, `type:bug`, and `defect` ([.github/LABELS.md](.github/LABELS.md))
- **Area labels**: Both old (`backend`, `infra`) and new (`area:api`, `area:db`, `area:infra`) conventions coexist ([.github/LABELS.md](.github/LABELS.md))
- **Status labels**: `good first issue` vs. `good-first-issue` variants ([.github/LABELS.md](.github/LABELS.md))

**Evidence:**
- [.github/LABELS.md](.github/LABELS.md) explicitly documents "inconsistently used" patterns across `bug`, `type:bug`, `defect`, `incident`, `sev1`, `priority-high`, etc.
- **Issue #104**: Opened to clarify severity levels but remains open ([.github/ISSUES.md](.github/ISSUES.md))
- **Issue #108**: Meta-issue to align label usage notes that mixing labels "makes reporting confusing" ([.github/ISSUES.md](.github/ISSUES.md))

**Implications:**
Inconsistent labeling makes filtering, reporting, and automation difficult. This is a known issue (meta-tracked in Issue #108) but not yet resolved.

### 5. Written Guidelines vs. Reality: Documentation Debt

Multiple instances show documented intent differs from practice:

| Area | Documented | Actual Behavior | Evidence |
|------|-----------|-----------------|----------|
| **Incident postmortems** | Must be in [ops/incidents.md](ops/incidents.md) | Often in comments, Slack, or weekly sync notes | Issue #101, #102; [ops/incidents.md](ops/incidents.md) |
| **Issue-PR linking** | PRs "should" link issues with `Fixes #<id>` | PR #210, #213 have no formal issue link until retroactive | [.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md) |
| **CI gates** | PRs "should" pass CI before merge | PR #213 merged with failing tests via admin override | [.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md) |
| **Canary deployments** | Not documented | PR #210 discussion reveals "we don't really have a documented canary process yet" | [.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md) |
| **Deprecation windows** | Informally discussed (6 months) | PR #220: "agreed in last architecture review but not written down" | [docs/api_versioning.md](docs/api_versioning.md), [.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md) |
| **DB migration rollbacks** | Not specified | Issue #101: "we usually don't roll back... but this is not codified" | [.github/ISSUES.md](.github/ISSUES.md) |

**Systemic Pattern:**
- [docs/api_versioning.md](docs/api_versioning.md): "Gaps & Open Questions" section acknowledges ambiguities
- [docs/architecture.md](docs/architecture.md): "In practice, not all of these rules are consistently followed, especially under time pressure"
- [PR #221](PR #221): Attempts to align [ops/incidents.md](ops/incidents.md) with reality; comment notes it "differs from CONTRIBUTING.md. We need a decision on which is source of truth"

## Recommendations for New Contributors

### For Backend Engineers

1. **Understand that written rules are guidelines, not gates:** Review [CONTRIBUTING.md](CONTRIBUTING.md) for intent, but observe recent PR patterns (especially [.github/PULL_REQUESTS.md](.github/PULL_REQUESTS.md)) to understand actual practice.

2. **Coordinate early for risky changes:** If your work touches DB schema, connection pooling, or API semantics, discuss in issue comments before opening a PR. There is no formal approval process, so building consensus ahead of time prevents merge delays.

3. **Label consistency is aspirational:** Use current standard labels (`area:api`, `sev1`), but don't be surprised if older issues use different conventions. Refer to [.github/LABELS.md](.github/LABELS.md) for context.

4. **Incidents override process:** During Sev1 incidents, expect rapid decision-making, admin overrides of CI, and deferred documentation. Follow up post-incident to ensure lessons are captured.

### For SREs & Platform Engineers

1. **Oncall has broad authority:** The oncall person effectively makes final decisions during incidents, even outside their usual domain. This is not explicitly documented but is the de facto practice (see Issue #105, PR #213).

2. **Rollback policies are informal:** DB migration rollbacks are rare and decided case-by-case. Application rollbacks are common but not always paired with DB rollbacks (Issue #101).

3. **Escalation happens in Slack:** GitHub issues are created retroactively for audit purposes. Real-time coordination is in Slack, so ensure you're in the right channels.

4. **Documentation debt is acknowledged:** [ops/oncall.md](ops/oncall.md) and [ops/incidents.md](ops/incidents.md) are "slightly out of date" and "not fully in sync with... actual practice". Treat them as historical references, not current truth.

### For All Contributors

1. **Check recent issues/PRs, not just docs:** The most reliable guide to current process is the last 3-6 months of issues and PRs, particularly incidents and hotfixes.

2. **Ask "who decides?" early:** For breaking changes, schema migrations, or deprecations, explicitly ask in issue comments who has final approval. Don't assume it's documented.

3. **Contribute to normalization efforts:** Issues #104 (severity levels), #108 (label alignment), and PR #221 (incident docs) are ongoing efforts to close the gap between docs and practice. Contributions welcome.

4. **Expect process flexibility:** This repository values shipping fixes quickly over strict process adherence, especially under pressure. Use your judgment and document decisions after the fact.

## Conclusion

The Todo API repository exhibits a pragmatic, high-trust collaboration culture where teams prioritize solving problems over following documented process. This works well for experienced contributors but creates friction for newcomers who may assume written guidelines are authoritative.

Key tensions:
- **Velocity vs. process:** Teams bypass gates during incidents, then struggle to update documentation afterward
- **Informal vs. formal:** Important decisions (approval authority, deprecation timelines, rollback policies) are made verbally and not reliably captured
- **Role boundaries:** Backend and SRE responsibilities overlap significantly in practice, more than docs suggest

To work effectively here, new contributors should focus on observing recent behavior patterns, asking clarifying questions early, and accepting that documentation will lag behind practice.
