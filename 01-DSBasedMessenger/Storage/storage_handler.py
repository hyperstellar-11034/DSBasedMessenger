import json
from datetime import datetime
from Models.user import User  
from Models.message import Message  
from DataStructures.linked_list import ReplyList

class StorageHandler:
    @staticmethod
    def save_all(file_path, users_table, message_tree, replies_table):
        data = {
            "users": [],
            "messages": [],
            "replies": []
        }

        # Save users from HashTable
        for chain in users_table.chains_list:
            p = chain.head
            while p:
                user_dict = {
                    "id": p.user_id,
                    "name": p.user_values[0],
                    "job": p.user_values[1]
                }
                data["users"].append(user_dict)
                p = p.next

        # Save messages from BST
        def collect_messages(node):
            if node is None:
                return
            collect_messages(node.left)
            data["messages"].append({
                "timestamp": node.timestamp,
                "content": node.message_text["text"],
                "sender_id": node.message_text["sender_id"],
                "reply_to": node.message_text["reply_to"]
            })
            collect_messages(node.right)

        collect_messages(message_tree.root)

        # Save replies from replies_table (HashTable)
        for chain in replies_table.chains_list:
            p = chain.head
            while p:
                timestamp = p.user_id
                reply_list = p.user_values  # this is a ReplyList
                replies = reply_list.get_all_replies()
                data["replies"].append({
                    "timestamp": timestamp,
                    "replies": replies
                })
                p = p.next

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_all(file_path, users_table, message_tree, replies_table):
        with open(file_path, "r") as f:
            data = json.load(f)

        # Load users into HashTable
        for u in data["users"]:
            users_table.insert(u["id"], (u["name"], u["job"]))

        # Load messages into BST
        for m in data["messages"]:
            timestamp = m["timestamp"]
            message_text = {
                "text": m["content"],
                "sender_id": m["sender_id"],
                "reply_to": m["reply_to"]
            }
            message_tree.root = message_tree.insert(message_tree.root, timestamp, message_text)

        # Load replies into HashTable of ReplyLists
        for r in data["replies"]:
            reply_list = ReplyList()
            for reply in r["replies"]:
                reply_list.add_reply(reply)
            replies_table.insert(r["timestamp"], reply_list)
