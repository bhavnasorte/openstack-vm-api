from flask import Blueprint, request
from app.services.openstack_client import OpenStackClient
from app.utils.response_helper import success, error

vm_bp = Blueprint("vms", __name__)
client = OpenStackClient()

REQUIRED_FIELDS = ["name", "flavor", "image"]


@vm_bp.route("/vms", methods=["POST"])
def create_vm():
    body = request.get_json()
    if not body:
        return error("Request body is required", 400)
    missing = [f for f in REQUIRED_FIELDS if not body.get(f)]
    if missing:
        return error(f"Missing required fields: {', '.join(missing)}", 422)
    vm = client.create_vm(
        name=body["name"],
        flavor=body["flavor"],
        image=body["image"],
        network=body.get("network"),
    )
    return success(vm.to_dict(), 201)


@vm_bp.route("/vms", methods=["GET"])
def list_vms():
    vms = client.list_vms()
    return success([vm.to_dict() for vm in vms])


@vm_bp.route("/vms/<vm_id>", methods=["GET"])
def get_vm(vm_id):
    vm = client.get_vm(vm_id)
    if not vm or vm.status == "DELETED":
        return error("VM not found", 404)
    return success(vm.to_dict())


@vm_bp.route("/vms/<vm_id>/start", methods=["POST"])
def start_vm(vm_id):
    vm, err = client.start_vm(vm_id)
    if err:
        code = 404 if "not found" in err else 409
        return error(err, code)
    return success(vm.to_dict())


@vm_bp.route("/vms/<vm_id>/stop", methods=["POST"])
def stop_vm(vm_id):
    vm, err = client.stop_vm(vm_id)
    if err:
        code = 404 if "not found" in err else 409
        return error(err, code)
    return success(vm.to_dict())


@vm_bp.route("/vms/<vm_id>", methods=["DELETE"])
def delete_vm(vm_id):
    ok, err = client.delete_vm(vm_id)
    if not ok:
        code = 404 if "not found" in err else 409
        return error(err, code)
    return success({"message": f"VM {vm_id} deleted successfully"})
