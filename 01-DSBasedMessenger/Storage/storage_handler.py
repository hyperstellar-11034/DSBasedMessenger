import json #is used to read/write JSON files
import os #is used to check if the storage file exists
from Models.user import User
from DataStructures.hashtable import HashTable

class StorageHandler:
    def __init__(self, storage_file='users_data.json'):
        self.storage_file = storage_file
        self.users_table = HashTable()  #creates a hash table 
        self.load_users()

    def load_users(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                for user_dict in data.get('users', []):
                    user = User.from_dict(user_dict)
                    self.users_table.insert(user.key, user)
        else:
            # empty hash table
            self.users_table = HashTable()

    def save_users(self):
        # Extract all users from hash table chains
        all_users = []
        for chain in self.users_table.chains_list:
            node = chain.head
            while node:
                all_users.append(node.user_values.to_dict())
                node = node.next
        with open(self.storage_file, 'w') as f:
            json.dump({"users": all_users}, f, indent=4)

    def add_user(self, user: User):
        # Check if user with same phone number exists
        existing_user = self.get_user_by_phone(user.phone_number)
        if existing_user:
            raise ValueError("User with this phone number already exists.")
        self.users_table.insert(user.key, user)
        self.save_users()

    def get_user_by_phone(self, phone_number: str):
        key = User._hash_phone_number(phone_number)
        chain = self.users_table.chains_list[key]
        node = chain.head
        while node:
            if node.user_values.phone_number == phone_number:
                return node.user_values
            node = node.next
        return None

    def update_user(self, user: User):
        # Replace user in hash table chain
        key = user.key
        chain = self.users_table.chains_list[key]
        node = chain.head
        while node:
            if node.user_values.phone_number == user.phone_number:
                node.user_values = user
                self.save_users()
                return
            node = node.next
        raise ValueError("User does not exist.")

    def get_all_users(self):
        all_users = []
        for chain in self.users_table.chains_list:
            node = chain.head
            while node:
                all_users.append(node.user_values)
                node = node.next
        return all_users
