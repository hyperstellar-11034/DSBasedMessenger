import uuid

class User:
    def __init__(self, phone_number, name):
        if not self._validate_phone_number(phone_number):
            raise ValueError("Phone number must be exactly 11 digits")
        self.phone_number = phone_number
        self.name = name
        self.key = self._hash_phone_number(phone_number)  # integer key for hash table
        self.contacts = []  
        self.messages = []  

    @staticmethod
    def _validate_phone_number(phone_number):
        return isinstance(phone_number, str) and phone_number.isdigit() and len(phone_number) == 11

    @staticmethod
    def _hash_phone_number(phone_number):
        # Simple hash function: sum of digits mod 17 
        return sum(int(d) for d in phone_number) % 17

    def update_contact(self, name=None):
        if name is not None:
            print(f"Updating name from '{self.name}' to '{name}'")
            self.name = name

    def add_contact(self, contact_phone_number):
        # Add contact only if not already in contacts
        if contact_phone_number not in self.contacts:
            self.contacts.append(contact_phone_number)

    def to_dict(self):
        return {
            "key": self.key,
            "phone_number": self.phone_number,
            "name": self.name,
            "contacts": self.contacts,
        }

    @staticmethod
    def from_dict(d):
        user = User(d["phone_number"], d["name"])
        user.key = d["key"]
        user.contacts = d.get("contacts", [])
        return user
