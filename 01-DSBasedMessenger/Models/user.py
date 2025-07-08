import uuid

class User:
    def __init__(self, name, job):
        self.id = self.generate_unique_id()
        self.name = name
        self.job = job

    @staticmethod
    def generate_unique_id():
        # Generate a unique int ID by converting part of UUID4
        return int(uuid.uuid4().hex[:8], 16)

    def update_contact(self, name, job):
        if name is not None:
            print(f"Updating name from '{self.name}' to '{name}'")
            self.name = name
        if job is not None:
            print(f"Updating job from '{self.job}' to '{job}'")
            self.job = job

    def to_dict(self):
        return {"id": self.id, "name": self.name, "job": self.job}

    @staticmethod
    def from_dict(d):
        user = User(d["name"], d["job"])
        user.id = d["id"]
        return user
