class Account:
    def __init__(self, source: str, login: str, password: str, id: int = None):
        self.id = id
        self.source = source
        self.login = login
        self.password = password

    def __str__(self):
        return f"(id={self.id}, source={self.source}, login={self.login}, password={self.password})"


class User:
    def __init__(self, username: str, password: bytes, id: int = None):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return f"(id={self.id}, user_name={self.username}, password={self.password})"
