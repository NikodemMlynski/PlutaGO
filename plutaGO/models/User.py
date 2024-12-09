
class User:
    def __init__(self, id, name, surname, email, password, role, amount_of_pluts):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.role = role
        self.amount_of_pluts = amount_of_pluts
    
    def increase_pluts(self, amount_of_pluts):
        self.amount_of_pluts += amount_of_pluts
    
    def make_payment(self, amount_of_pluts):
        self.amount_of_pluts -= amount_of_pluts

