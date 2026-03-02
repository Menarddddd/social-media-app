from uuid import UUID


class GenericException(Exception):
    def __init__(self, message: str):
        self.message = message


class LoginException(Exception):
    def __init__(self, username: str):
        self.username = username


class PasswordException(Exception):
    pass


class EntityNotFoundException(Exception):
    def __init__(self, entity: str, id: UUID):
        self.entity = entity
        self.id = id

    def __str__(self):
        return f"{self.entity} not found"


class DuplicateEntryException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value

    def __str__(self):
        return f"{self.field} exist already"


class TokenException(Exception):
    def __init__(self, message):
        self.message = message
