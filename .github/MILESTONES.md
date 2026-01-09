# Milestones Overview

## v1.3.0 - Stability & Observability

**Target:** 2025-Q2

**Goals:**
- Reduce incident frequency related to DB timeouts and worker stalls
- Add basic tracing and better logging for background jobs

**Relevant Issues (representative):**
- #101 - `GET /todos` intermittently returns 500 in production
- #102 - Background worker stuck processing stale tasks
- #107 - Add tracing for background workers

---

## v1.2.0 - Multi-Tenancy

**Released:** 2024-09

Highlights:
- Per-user todo lists
- Tenant-aware database schema

---

## v1.1.0 - API Polish

**Released:** 2024-05

Highlights:
- Better input validation
- Improved error responses

---

## v1.0.0 - Initial Release

**Released:** 2024-01

Highlights:
- Basic CRUD for todos
- Simple auth stub (not production-ready)
