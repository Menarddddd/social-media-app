from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import Base, engine
from app.config.setup import register_routers, register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

register_routers(app)
register_exception_handlers(app)
