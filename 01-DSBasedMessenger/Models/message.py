from datetime import datetime, timezone

class Message:
    def __init__(self, sender_id, content, timestamp=None, reply_to=None):
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp if timestamp is not None else self.generate_timestamp()
        self.reply_to = reply_to  

    def generate_timestamp(self):
        return datetime.now(timezone.utc)

    def update_content(self, new_content):
        print("Updating message content from '{}' to '{}'".format(self.content, new_content))
        self.content = new_content
        self.timestamp = self.generate_timestamp()

    def __str__(self):
        return "[{}] User {}: {}".format(self.timestamp.isoformat(), self.sender_id, self.content)

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "reply_to": self.reply_to
        }

    @staticmethod
    def from_dict(d):
        timestamp = datetime.fromisoformat(d["timestamp"])
        return Message(d["sender_id"], d["content"], timestamp=timestamp, reply_to=d.get("reply_to"))
