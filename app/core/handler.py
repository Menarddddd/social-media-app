from typing import cast

from fastapi import status, Request
from fastapi.responses import JSONResponse

from app.core.exception import EntityNotFoundException


def entity_not_found_handler(request: Request, exc: Exception):
    exc = cast(EntityNotFoundException, exc)

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={f"{exc.entity}_id": str(exc.id), "message": str(exc)},
    )
