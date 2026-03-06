from typing import Mapping

from sqlalchemy.exc import IntegrityError


class InvalidCredentialsError(Exception):
    pass


class FieldNotFoundException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value

    def __str__(self):
        return f"{self.field} not found"


class DuplicateEntryException(Exception):
    def __init__(self, field: str, value: str | None):
        self.field = field
        self.value = value
        super().__init__(f"Duplicate {field}: {value}")


# Exception Helper Function
def get_unique_constraint_name(e: IntegrityError) -> str | None:
    orig = e.orig
    return getattr(orig, "constraint_name", None)


UNIQUE_CONSTRAINT_TO_FIELD = {
    "uq_users_email": "email",
    "uq_users_username": "username",
}


def raise_duplicate_from_integrity_error(
    e: IntegrityError,
    values: Mapping[str, str | None],
) -> None:
    constraint = get_unique_constraint_name(e)

    if constraint is None:
        return

    field = UNIQUE_CONSTRAINT_TO_FIELD.get(constraint)

    if field:
        raise DuplicateEntryException(field, values.get(field)) from e
