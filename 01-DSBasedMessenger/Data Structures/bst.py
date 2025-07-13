from datetime import datetime

class Node:
    def __init__(self, timestamp, message_text):
        self.timestamp = timestamp  # int timestamp (UNIX time)
        self.message_text = message_text  
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def search(self, node, timestamp):  # recursive
        if node is None:
            return None

        if timestamp == node.timestamp:
            return node.message_text
        elif timestamp < node.timestamp:
            return self.search(node.left, timestamp)
        else:
            return self.search(node.right, timestamp)

    def insert(self, node, timestamp, message_text):
        if node is None:
            return Node(timestamp, message_text)

        if timestamp < node.timestamp:
            node.left = self.insert(node.left, timestamp, message_text)
        elif timestamp > node.timestamp:
            node.right = self.insert(node.right, timestamp, message_text)
        else:
            # Overwrite existing message with same timestamp
            node.message_text = message_text

        return node

    def delete(self, node, timestamp):
        if node is None:
            return None

        if timestamp < node.timestamp:
            node.left = self.delete(node.left, timestamp)
        elif timestamp > node.timestamp:
            node.right = self.delete(node.right, timestamp)
        else:
            # Node found — handle deletion
            if node.left is None and node.right is None:
                return None  # Leaf
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Two children: replace with inorder successor
                successor = self._find_inorder_successor(node.right)
                node.timestamp = successor.timestamp
                node.message_text = successor.message_text
                node.right = self.delete(node.right, successor.timestamp)

        return node

    def _find_inorder_successor(self, node):
    # The in-order successor: the smallest node in the right subtree
        current = node
        while current.left is not None:
            current = current.left
        return current

    def traverse(self, node):
        if node is None:
            return

        self.traverse(node.left)

        # Convert int timestamp to readable format
        timestamp_str = datetime.fromtimestamp(node.timestamp).isoformat()
        message_str = node.message_text
        print(f"Timestamp: {timestamp_str}, Message: {message_str}")

        self.traverse(node.right)
