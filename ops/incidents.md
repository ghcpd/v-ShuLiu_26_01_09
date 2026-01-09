# Incident Log (Partial)

This file is **intended** to record major production incidents and their follow-up actions. In practice, not all incidents are documented here.

---

## Incident 2024-10-01: `GET /todos` 500 Errors

- **Severity:** Sev1 (customer-visible outage)
- **Summary:** Increased 500 error rates on `GET /todos` after deploying PR #210.
- **Timeline (rough):**
  - 10:05 - Alert fired (error rate > 5%)
  - 10:10 - Oncall SRE investigated logs
  - 10:20 - Manual rollback of application deployment (DB migration not rolled back)
  - 11:00 - Temporary stabilization

- **Follow-up:**
  - PR #213 proposed as permanent fix (DB timeouts, retries)
  - No separate GitHub issue was created at the time; Issue #101 was filed retroactively
  - Some discussion happened in Slack and was not fully copied here

**Action Items (intended):**
- Document rollback policies for DB migrations
- Clarify when to open an `incident`-labeled issue

Status of action items: **Partially addressed, not formally closed.**

---

## Incident 2024-11-12: Background Worker Stalls

- **Severity:** Marked as Sev1 in oncall notes, but only tagged as `sev-1` in GitHub Issue #102
- **Summary:** Background worker repeatedly processed stale tasks, causing duplicate reminders.

- **Follow-up:**
  - PR #215 fixed the worker logic
  - No dedicated postmortem entry was added initially; notes were mentioned in a weekly ops sync

This reflects the need to better align oncall notes, GitHub labels, and this log.
