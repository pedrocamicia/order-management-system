class User:
    def __init__(self, id : int | None, email : str, hashed_password : str, role : str | None):
        self.id = id,
        self.email = email
        self.hashed_password = hashed_password
        self.role = role