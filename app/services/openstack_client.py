from datetime import datetime
from app.models.vm import VM

_vm_store = {}

class OpenStackClient:

    def create_vm(self, name, flavor, image, network=None):
        vm = VM(name=name, flavor=flavor, image=image, network=network)
        vm.status = "ACTIVE"
        _vm_store[vm.id] = vm
        return vm

    def list_vms(self):
        return [vm for vm in _vm_store.values() if vm.status != "DELETED"]

    def get_vm(self, vm_id):
        return _vm_store.get(vm_id)

    def start_vm(self, vm_id):
        vm = _vm_store.get(vm_id)
        if not vm:
            return None, "VM not found"
        if vm.status == "ACTIVE":
            return None, "VM is already running"
        if vm.status == "DELETED":
            return None, "Cannot start a deleted VM"
        vm.status = "ACTIVE"
        vm.updated_at = datetime.utcnow().isoformat()
        return vm, None

    def stop_vm(self, vm_id):
        vm = _vm_store.get(vm_id)
        if not vm:
            return None, "VM not found"
        if vm.status == "STOPPED":
            return None, "VM is already stopped"
        if vm.status == "DELETED":
            return None, "Cannot stop a deleted VM"
        vm.status = "STOPPED"
        vm.updated_at = datetime.utcnow().isoformat()
        return vm, None

    def delete_vm(self, vm_id):
        vm = _vm_store.get(vm_id)
        if not vm:
            return False, "VM not found"
        if vm.status == "DELETED":
            return False, "VM already deleted"
        vm.status = "DELETED"
        vm.updated_at = datetime.utcnow().isoformat()
        return True, None
