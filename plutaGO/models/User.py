import re  # Import for email validation

class User:
    def __init__(self, id, name, surname, email, password, role):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.role = role

