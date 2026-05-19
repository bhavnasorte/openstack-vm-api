# openstack-vm-api

A REST API to manage OpenStack VM lifecycle built as part of an engineering assessment.

## What this does

You can use this API to create, list, start, stop, and delete virtual machines.
The OpenStack SDK is mocked with in-memory state for now, but the service layer
is designed so you can swap in the real SDK without touching the routes.

## Why Flask?

I picked Flask because it stays out of your way. No magic, no hidden behavior,
just routes, request, response. Easy to test, easy to read.

## Project Structure

    app/
    routes/      - URL endpoints, request parsing
    services/    - OpenStack SDK calls (mocked for now)
    models/      - VM data model
    utils/       - shared response helpers

## How to run it

    git clone https://github.com/bhavnasorte/openstack-vm-api.git
    cd openstack-vm-api
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    python run.py

Server starts at http://localhost:5000

## Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | /health | Check if server is up |
| POST | /api/v1/vms | Create a new VM |
| GET | /api/v1/vms | List all VMs |
| GET | /api/v1/vms/{id} | Get one VM by ID |
| POST | /api/v1/vms/{id}/start | Start a stopped VM |
| POST | /api/v1/vms/{id}/stop | Stop a running VM |
| DELETE | /api/v1/vms/{id} | Delete a VM |

## Quick test

    # create
    curl -X POST http://localhost:5000/api/v1/vms \
      -H "Content-Type: application/json" \
      -d '{"name":"my-vm","flavor":"m1.small","image":"ubuntu-22.04"}'

    # list
    curl http://localhost:5000/api/v1/vms

    # stop
    curl -X POST http://localhost:5000/api/v1/vms/{id}/stop

    # delete
    curl -X DELETE http://localhost:5000/api/v1/vms/{id}

## Response format

Every response looks the same whether success or error:

    { "data": { ... }, "error": null }

## Running tests

    pytest tests/ -v

7 tests covering create, list, get, stop, start, delete and conflict cases.

## VM states

    PENDING -> ACTIVE -> STOPPED -> DELETED

- You cannot start an already running VM, returns 409
- You cannot stop an already stopped VM, returns 409
- Deleted VMs return 404

## What I would build next

- Real OpenStack SDK, the swap would only touch services/openstack_client.py
- JWT auth and role based access
- Async jobs, create and delete are slow in real OpenStack, should return a job ID to poll
- Pagination on the list endpoint
- Persistent storage, replace in-memory dict with PostgreSQL
- Docker and docker-compose for easy local setup
- Rate limiting
- Prometheus metrics

## Architecture

See docs/ARCHITECTURE.md for the full design writeup.


---
Built by Bhavna Sorte
