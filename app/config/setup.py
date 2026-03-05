from fastapi import FastAPI

from app.routers.ai import router as ai_router
from app.routers.user import router as user_router
from app.routers.post import router as post_router
from app.routers.comment import router as comment_router
from app.exceptions.exception import (
    EntityNotFoundException,
    DuplicateEntryException,
    GenericException,
    LoginException,
    TokenException,
)
from app.exceptions.handler import (
    entity_not_found_handler,
    duplicate_entry_exception_handler,
    login_exception_handler,
    token_exception_handler,
    generic_exception_handler,
)


def register_routers(app: FastAPI):
    app.include_router(ai_router, prefix="/api/ai", tags=["bot"])
    app.include_router(user_router, prefix="/api/users", tags=["users"])
    app.include_router(post_router, prefix="/api/posts", tags=["posts"])
    app.include_router(comment_router, prefix="/api/comments", tags=["comment"])


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(GenericException, generic_exception_handler)
    app.add_exception_handler(LoginException, login_exception_handler)
    app.add_exception_handler(EntityNotFoundException, entity_not_found_handler)
    app.add_exception_handler(
        DuplicateEntryException, duplicate_entry_exception_handler
    )
    app.add_exception_handler(TokenException, token_exception_handler)
