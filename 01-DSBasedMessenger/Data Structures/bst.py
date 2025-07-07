class Node:
    def __init__(self, timestamp, message_text):
        self.timestamp = timestamp
        self.message_text = message_text
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def search(self, node, timestamp): #recursive
        if node is None:
            return None
        
        if timestamp == node.timestamp:
            return node.message_text
        elif timestamp < node.timestamp:
            return self.search(node.left, timestamp)
        else:
            return self.search(node.right, timestamp)

    def insert(self, node, timestamp, message_text):
        #base case - empty node found, create new node.
        if node is None:
            return Node(timestamp, message_text)
        
        if timestamp < node.timestamp:
            node.left = self.insert(node.left, timestamp, message_text)
        elif timestamp > node.timestamp:
            node.right = self.insert(node.right, timestamp, message_text)
        else:
            # Timestamp already exists --> do nothing
            node.message_text = message_text
            
        return node

    def delete(self, node, timestamp):
        if node is None:  # Nothing to delete
            return None  

        # Navigating the tree to find the node to delete
        if timestamp < node.timestamp:
            node.left = self.delete(node.left, timestamp)
        elif timestamp > node.timestamp:
            node.right = self.delete(node.right, timestamp)
        else:
            # Node found, now handling deletion cases:

            # 1: leaf
            if node.left is None and node.right is None:
                return None  #simply remove that node

            # 2: Node has only right child
            elif node.left is None and node.right is not None:
                return node.right  # Replace node with right child

            # 3: Node has only left child
            elif node.right is None and node.left is not None:
                return node.left  # Replace node with left child

            # 4: Node has two children (it will automatically be our 'else')
            else:
                inorder_successor = self._find_inorder_successor(node.right) 
                #above said 'right' because successor must be bigger than node and L side is less; R is more.
                node.timestamp = inorder_successor.timestamp #copy
                node.message_text = inorder_successor.message_text
                node.right = self.delete(node.right, inorder_successor.timestamp) #delete the dupliacate

        return node #returns the root of the updated subtree and recursion goes on...

    def _find_inorder_successor(self, node):
        t = node #root
        while t.left is not None:
            t = t.left #loop. keeps going left and left until there is no more left left ;)
        return t
    '''so this function handles the "going left left..process" of the "right side" of node(root) --> successor
    the "right side" part gets handles when we call this function. there wechoose the argument as node.right'''
    
    def traverse(self, node): # in-order traversal to display messages sorted by timestamp
        if node is None:
            return
        
        # L
        self.traverse(node.left)
        
        # Visit (and print timestamp and message)
        timestamp_str = str(node.timestamp)
        message_str = node.message_text
        print("Timestamp: {}, Message: {}".format(timestamp_str, message_str))
        
        # R
        self.traverse(node.right)
