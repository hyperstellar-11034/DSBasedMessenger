from datetime import datetime, timezone

class Message:
    def __init__(self, sender_id, content, timestamp=None):
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp if timestamp is not None else self.generate_timestamp()

    def generate_timestamp(self):
        return datetime.now(timezone.utc)

    def update_content(self, new_content):
        print("Updating message content from '{}' to '{}'".format(self.content, new_content))
        self.content = new_content
        self.timestamp = self.generate_timestamp()

    def __str__(self):
        return "[{}] User {}: {}".format(self.timestamp.isoformat(), self.sender_id, self.content)
