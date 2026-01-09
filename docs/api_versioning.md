# API Versioning Guidelines (Draft)

This document describes the **intended** approach to API versioning for the Todo API Service.

## Principles

- Avoid breaking changes to existing endpoints whenever possible
- When breaking changes are necessary:
  - Introduce a new versioned path (e.g., `/v2/todos`)
  - Maintain old versions for at least one deprecation window (e.g., 6 months)
  - Document changes clearly in API docs and RELEASE_NOTES

## Current State

- `/v1/todos` is the default public API
- `/v2/todos` is being introduced for more flexible responses (see PR #220)

## Gaps & Open Questions

- The deprecation window is discussed informally (e.g., "6 months") but not formally agreed in any governing doc
- It's unclear who has final authority to approve a breaking change:
  - Backend lead?
  - Product owner?
  - Architecture review group?

These ambiguities show up in issue and PR discussions.
