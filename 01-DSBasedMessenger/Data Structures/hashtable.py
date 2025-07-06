class Node:
    def __init__(self, user_id, user_values):
        self.user_id = user_id       
        self.user_values = user_values  
        self.next = None     
        
class Chain:
    def __init__(self, chain_id):
        self.chain_id = chain_id 
        self.head = None  
    
    def search(self, user_id):
        p = self.head
        while p: #true means not None
            if p.user_id == user_id:
                return p.user_values
            p = p.next
        return None
    
    def delete(self, user_id):
        p = self.head
        prev = None #initially
        while p:    #as long as p isn't None
            if p.user_id == user_id:
                if prev is None: #means we're at head node
                    # Deleting the head node
                    self.head = p.next
                else:
                    # Bypass the node to delete it
                    prev.next = p.next
                return True 
            prev = p
            p = p.next
        return False  # User not found, nothing deleted
    
    def insert(self, user_id, user_values):
        # Insert new node at the head of the linked list
        new_node = Node(user_id, user_values)
        new_node.next = self.head #insert
        self.head = new_node
    
class HashTable:
    def __init__(self):
        self.size = 17

        self.chains_list = []
        for i in range(self.size):
            self.chains_list.append(Chain(i)) 

    def hash_function(self, user_id):
        return user_id % self.size

    def insert(self, user_id, user_values):
        index = self.hash_function(user_id)
        self.chains_list[index].insert(user_id, user_values)

    def get(self, user_id):
        chain_id = self.hash_function(user_id)
        return self.chains_list[chain_id].search(user_id)
    
    def delete(self, user_id):
        chain_id = self.hash_function(user_id)
        is_deleted = self.chains_list[chain_id].delete(user_id)
        if is_deleted:
            print("Successfully Deleted")
        else:
            print("User not found") 
