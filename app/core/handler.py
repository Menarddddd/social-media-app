from fastapi import status, Request
from fastapi.responses import JSONResponse

from app.core.exception import (
    EntityNotFoundException,
    DuplicateEntryException,
    GenericException,
    LoginException,
    TokenException,
)


def generic_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, GenericException)

    return JSONResponse(status_code=exc.status, content={"message": exc.message})


def login_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, LoginException)

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "username": exc.username,
            "message": "Username or password is incorrect",
        },
    )


def entity_not_found_handler(request: Request, exc: Exception):
    assert isinstance(exc, EntityNotFoundException)

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={f"{exc.entity.lower()}_id": str(exc.id), "message": str(exc)},
    )


def duplicate_entry_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, DuplicateEntryException)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={f"{exc.field}": exc.value, "message": str(exc)},
    )


def token_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, TokenException)

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )
