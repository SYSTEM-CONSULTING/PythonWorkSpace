from models.user import User
class UserService:
    def __init__(self):
        self.users=[User(1,'Bernhard','bd@example.com'),User(2,'Anna','anna@example.com')]
    def list_users(self): return self.users
