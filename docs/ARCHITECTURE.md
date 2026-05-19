# Architecture & Design Decisions

## Overview
REST API for managing OpenStack VM lifecycle operations built with Python and Flask.

## Tech Stack
| Component | Choice | Reason |
|-----------|--------|--------|
| Framework | Flask 3.1 | Lightweight, explicit routing, easy to test |
| OpenStack SDK | Mocked (swappable) | Abstracted behind a service layer for testability |
| Config | python-dotenv | 12-factor app pattern; no secrets in code |
| Testing | pytest + pytest-flask | Industry standard, simple fixtures |
| CI | GitHub Actions | Free, native GitHub integration |
| Linting | flake8 + black | Code quality and consistent formatting |

## Project Structure

    app/
    routes/         # HTTP layer - URL routing and request parsing
    services/       # Business logic - OpenStack SDK abstraction
    models/         # Data models - VM entity
    utils/          # Shared helpers - consistent JSON responses

## VM State Machine

    PENDING -> ACTIVE <-> STOPPED -> DELETED

- Created VMs start as PENDING, immediately transition to ACTIVE (simulated provisioning)
- Only ACTIVE VMs can be stopped
- Only STOPPED VMs can be started
- DELETED VMs cannot be started, stopped, or re-deleted

## API Design Choices
- RESTful resource-based URLs (/vms, /vms/{id})
- Actions (start/stop) use POST sub-resources (/vms/{id}/start) per REST best practices
- All responses return a consistent JSON envelope: {"data": ..., "error": ...}
- HTTP status codes strictly followed:
  - 200 OK - successful read/update
  - 201 Created - VM created
  - 404 Not Found - VM does not exist
  - 409 Conflict - invalid state transition
  - 422 Unprocessable Entity - missing required fields

## Abstraction Layer
The OpenStackClient service wraps all SDK calls. In this prototype it uses
an in-memory dictionary to simulate OpenStack state. Swapping to the real
OpenStack SDK requires changes only inside services/openstack_client.py -
routes and models are unaffected.

## Roadmap / Backlog
- [ ] JWT authentication and role-based access control
- [ ] Real OpenStack SDK integration via environment credentials
- [ ] Async job tracking - long-running operations return a job ID with polling endpoint
- [ ] Pagination and filtering on the VM list endpoint
- [ ] Rate limiting
- [ ] Prometheus metrics endpoint
- [ ] Docker + docker-compose for local development
- [ ] Persistent storage (PostgreSQL) to replace in-memory store
