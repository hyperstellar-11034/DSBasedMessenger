from datetime import datetime, timezone
from DataStructures.linked_list import ReplyList

class Message:
    def __init__(self, sender_id, receiver_id, content, timestamp=None, reply_to=None, replies=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.timestamp = timestamp or datetime.now(timezone.utc)
        self.reply_to = reply_to
        self.replies = replies or ReplyList()

    def generate_timestamp(self):
        return datetime.now(timezone.utc)

    def update_content(self, new_content):
        print(f"Updating message content from '{self.content}' to '{new_content}'")
        self.content = new_content
        self.timestamp = self.generate_timestamp()

    def __str__(self):
        return f"[{self.timestamp.isoformat()}] User {self.sender_id}: {self.content}"

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "reply_to": self.reply_to,
            "replies": [r.to_dict() for r in self.replies.get_all_replies()]
        }

    @staticmethod
    def from_dict(d):
        replies = ReplyList()
        for r in d.get("replies", []):
            replies.add_reply(Message.from_dict(r))
        timestamp = datetime.fromisoformat(d["timestamp"])
        return Message(
            sender_id=d["sender_id"],
            receiver_id=d.get("receiver_id"),
            content=d["content"],
            timestamp=timestamp,
            reply_to=d.get("reply_to"),
            replies=replies
        )
