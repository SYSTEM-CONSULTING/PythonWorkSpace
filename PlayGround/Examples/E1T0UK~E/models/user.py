class User:
    def __init__(self,uid,name,email): self.id=uid; self.name=name; self.email=email
    def __repr__(self): return f'<User {self.name}>'
