import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_create_vm_success(client):
    res = client.post("/api/v1/vms", json={
        "name": "test-vm", "flavor": "m1.small", "image": "ubuntu-22.04"
    })
    assert res.status_code == 201
    assert res.json["data"]["status"] == "ACTIVE"

def test_create_vm_missing_fields(client):
    res = client.post("/api/v1/vms", json={"name": "test-vm"})
    assert res.status_code == 422

def test_list_vms(client):
    res = client.get("/api/v1/vms")
    assert res.status_code == 200
    assert isinstance(res.json["data"], list)

def test_get_vm_not_found(client):
    res = client.get("/api/v1/vms/nonexistent-id")
    assert res.status_code == 404

def test_stop_and_start_vm(client):
    create_res = client.post("/api/v1/vms", json={
        "name": "vm-lifecycle", "flavor": "m1.medium", "image": "ubuntu-22.04"
    })
    vm_id = create_res.json["data"]["id"]
    stop_res = client.post(f"/api/v1/vms/{vm_id}/stop")
    assert stop_res.json["data"]["status"] == "STOPPED"
    start_res = client.post(f"/api/v1/vms/{vm_id}/start")
    assert start_res.json["data"]["status"] == "ACTIVE"

def test_delete_vm(client):
    create_res = client.post("/api/v1/vms", json={
        "name": "vm-to-delete", "flavor": "m1.small", "image": "ubuntu-22.04"
    })
    vm_id = create_res.json["data"]["id"]
    client.delete(f"/api/v1/vms/{vm_id}")
    get_res = client.get(f"/api/v1/vms/{vm_id}")
    assert get_res.status_code == 404

def test_double_stop_conflict(client):
    create_res = client.post("/api/v1/vms", json={
        "name": "vm-conflict", "flavor": "m1.small", "image": "ubuntu-22.04"
    })
    vm_id = create_res.json["data"]["id"]
    client.post(f"/api/v1/vms/{vm_id}/stop")
    res = client.post(f"/api/v1/vms/{vm_id}/stop")
    assert res.status_code == 409
