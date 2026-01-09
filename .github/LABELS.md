# Label Usage Overview

This document summarizes how labels are (inconsistently) used across issues and PRs in this repository.

## Bug / Incident Related Labels

Different patterns appear over time:

- `bug` — generic bug reports (older issues)
- `type:bug` — newer style type-prefixed bugs
- `defect` — occasionally used by QA contributors
- `incident` — intended for production incidents
- `sev1`, `sev2`, `sev3` — intended severity labels
- `priority-high`, `priority-medium` — used in some older issues instead of `sev*`

## Area / Component Labels

Multiple overlapping conventions:

- `backend` — generic backend label (old)
- `area:api` — newer convention for API surface
- `area:db` — database migrations, queries, performance
- `area:infra` — deployment, observability, CI/CD
- `infra` — older, generic label for infrastructure

## Status / Process Labels

- `in-progress` — sometimes added manually when someone starts working
- `blocked` — used rarely, no clear process
- `needs-triage` — introduced recently but not applied consistently

## Good First Issue / Help Wanted

- `good first issue` — used for simple bugs
- `good-first-issue` — hyphenated variant used in a few issues
- `help wanted` — tasks where maintainers explicitly want community help

We are working on normalizing these label conventions across the repository.
