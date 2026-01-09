# Todo API Service

A lightweight backend service for managing todo items, built with Python and FastAPI.

## Overview

- **Service name:** todo-api
- **Tech stack:**
  - Python 3.11
  - FastAPI
  - Uvicorn
  - PostgreSQL (production), SQLite (local/dev)
- **Core responsibilities:**
  - CRUD operations for todo items
  - Basic filtering and simple search
  - Per-user todo lists (multi-tenant)

## High-Level Architecture

See docs/architecture.md for a more detailed overview of components, dependencies, and data flow.

## Running Locally (Conceptual)

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Collaboration Context

Over time, more contributors (backend engineers, SREs, occasional product folks) have joined this repo. Processes have evolved organically:

- Some decisions are captured in docs/
- Some decisions only appear in issue / PR discussions
- Some are reflected through labels and milestones

## Contributing

See CONTRIBUTING.md for guidelines.
