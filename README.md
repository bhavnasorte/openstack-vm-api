# OpenStack VM Lifecycle API

A REST API prototype for managing OpenStack VM lifecycle operations — create, list, start, stop, and delete virtual machines.

## Tech Stack
- Python 3.11, Flask 3.1
- Mocked OpenStack SDK (swappable with real SDK)
- pytest + pytest-flask for testing
- GitHub Actions for CI
- flake8 + black for code quality

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/openstack-vm-api.git
cd openstack-vm-api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Server runs at `http://localhost:5000`

## Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | /health | Health check | 200 |
| POST | /api/v1/vms | Create a VM | 201 |
| GET | /api/v1/vms | List all VMs | 200 |
| GET | /api/v1/vms/{id} | Get VM details | 200 |
| POST | /api/v1/vms/{id}/start | Start a VM | 200 |
| POST | /api/v1/vms/{id}/stop | Stop a VM | 200 |
| DELETE | /api/v1/vms/{id} | Delete a VM | 200 |

## Example Usage

```bash
# Health check
curl http://localhost:5000/health

# Create a VM
curl -X POST http://localhost:5000/api/v1/vms \
  -H "Content-Type: application/json" \
  -d '{"name":"my-vm","flavor":"m1.small","image":"ubuntu-22.04"}'

# List all VMs
curl http://localhost:5000/api/v1/vms

# Get a VM
curl http://localhost:5000/api/v1/vms/{id}

# Stop a VM
curl -X POST http://localhost:5000/api/v1/vms/{id}/stop

# Start a VM
curl -X POST http://localhost:5000/api/v1/vms/{id}/start

# Delete a VM
curl -X DELETE http://localhost:5000/api/v1/vms/{id}
```

## Response Format

All responses follow a consistent envelope:

```json
{
  "data": { ... },
  "error": null
}
```

## Running Tests

```bash
pytest tests/ -v
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full design decisions, VM state machine, and tech stack rationale.

## Roadmap / Backlog
- [ ] JWT authentication and role-based access control
- [ ] Real OpenStack SDK integration
- [ ] Async job tracking with polling endpoint
- [ ] Pagination and filtering on VM list
- [ ] Rate limiting
- [ ] Prometheus metrics
- [ ] Docker + docker-compose
- [ ] Persistent storage (PostgreSQL)
