# Oncall & Escalation (Informal Notes)

This file informally describes oncall expectations. It has not been kept fully in sync with CONTRIBUTING.md or actual practice.

## Rotation

- Weekly rotation among backend engineers
- SREs provide backup for infrastructure-related issues

## Expectations

- For Sev1 incidents:
  - Oncall must respond within 15 minutes
  - Open an `incident`-labeled GitHub issue
  - Tag with `sev1` and relevant area labels (`area:api`, `area:db`, `area:infra`)
  - Schedule a post-incident review within 3 business days

## Reality (based on recent incidents)

- Some Sev1 incidents (e.g., worker stalls) never got a formal postmortem
- Severity labels used in issues vary (`sev1`, `sev-1`, `priority-high`)
- Escalation often happens in Slack without a consistent GitHub trail


