import uuid
from datetime import datetime

class VM:
    def __init__(self, name, flavor, image, network=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.flavor = flavor
        self.image = image
        self.network = network or "default"
        self.status = "PENDING"
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "flavor": self.flavor,
            "image": self.image,
            "network": self.network,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
