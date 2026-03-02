import jwt
from uuid import UUID
from typing import Annotated
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exception import (
    EntityNotFoundException,
    ForbiddenException,
    TokenException,
)
from app.core.database import get_db
from app.core.settings import settings
from app.models.user import User, Role
from app.repositories.post import get_post_by_id_db
from app.repositories.user import get_user_by_id_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise TokenException("Invalid token payload")

        user = await get_user_by_id_db(user_id, db)

        if not user:
            raise EntityNotFoundException("User", user_id)

        return user

    except jwt.ExpiredSignatureError:
        raise TokenException("Expired token")

    except jwt.PyJWTError:
        raise TokenException("Invalid token")


async def post_ownership(
    post_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = await get_post_by_id_db(post_id, db)
    if post is None:
        raise EntityNotFoundException("Post", post_id)

    if post.user_id != current_user.id:
        raise ForbiddenException("You do not own this post")

    return post


def required_role(require_role: Role):
    def role_checker(current_user: Annotated[User, Depends(get_current_user)]):
        if require_role != current_user.role:
            raise ForbiddenException("You are not an admin")
        return current_user

    return role_checker
