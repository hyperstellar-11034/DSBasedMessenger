import uuid #to generate unique user_id s  (?)

class User:
    def __init__(self, name, job, user_id):
        self.id = user_id if user_id is not None else self.generate_unique_id()
        self.name = name
        self.job = job

    @staticmethod #???
    def generate_unique_id():
        # Generate a unique int ID by converting part of a UUID4 string to int
        return int(uuid.uuid4().hex[:8], 16)

    def update_contact(self, name, job):
        if name is not None:
            print(f"Updating name from '{self.name}' to '{name}'")
            self.name = name
        if job is not None:
            print(f"Updating job from '{self.job}' to '{job}'")
            self.job = job
