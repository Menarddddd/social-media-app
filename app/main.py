from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import Base, engine
from app.routers.user import router as user_router
from app.routers.post import router as post_router
from app.core.exception import (
    EntityNotFoundException,
    DuplicateEntryException,
    GenericException,
    LoginException,
    PasswordException,
    TokenException,
)
from app.core.handler import (
    entity_not_found_handler,
    duplicate_entry_exception_handler,
    generic_exception_handler,
    login_exception_handler,
    password_exception_handler,
    token_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(GenericException, generic_exception_handler)
app.add_exception_handler(LoginException, login_exception_handler)
app.add_exception_handler(PasswordException, password_exception_handler)
app.add_exception_handler(EntityNotFoundException, entity_not_found_handler)
app.add_exception_handler(DuplicateEntryException, duplicate_entry_exception_handler)
app.add_exception_handler(TokenException, token_exception_handler)

app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(post_router, prefix="/api/posts", tags=["posts"])
