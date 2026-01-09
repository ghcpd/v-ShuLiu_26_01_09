# Architecture Overview

The Todo API Service is a monolithic backend that exposes a RESTful API for managing todo items.

## Components

- **API Layer (FastAPI)**
  - Defines HTTP endpoints (e.g., `GET /todos`, `POST /todos`, `PATCH /todos/{id}`)
  - Handles authentication and basic request validation

- **Service Layer**
  - Encapsulates business logic (e.g., tenant scoping, soft deletes)

- **Persistence Layer**
  - Uses an ORM to interact with PostgreSQL in production
  - Uses SQLite in development for convenience

- **Background Workers**
  - Process recurring tasks (e.g., reminders, cleanups)
  - Run as a separate process or container

## Operational Concerns

- Deployments are **intended** to go through staging before production
- API changes **should** follow the versioning guidelines in docs/api_versioning.md
- Incidents **should** be recorded in ops/incidents.md and linked to issues/PRs

In practice, not all of these rules are consistently followed, especially under time pressure during incidents.
