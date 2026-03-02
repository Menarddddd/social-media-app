from uuid import UUID
from fastapi import status


class GenericException(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message


class UnprocessableException(GenericException):
    def __init__(self, message):
        super().__init__(status.HTTP_422_UNPROCESSABLE_CONTENT, message)


class BadRequestException(GenericException):
    def __init__(self, message):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class ForbiddenException(GenericException):
    def __init__(self, message):
        super().__init__(status.HTTP_403_FORBIDDEN, message)


class LoginException(Exception):
    def __init__(self, username: str):
        self.username = username


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
