from uuid import UUID
from typing import Annotated, List

from fastapi.routing import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, post_ownership, required_role
from app.core.database import get_db
from app.models.post import Post
from app.models.user import User, Role
from app.schemas.post import PostCreate, PostOnlyResponse, PostResponse, PostUpdate
from app.services.post import (
    create_post_service,
    delete_post_admin_service,
    delete_post_service,
    feed_post_service,
    get_post_service,
    my_posts_service,
    update_post_service,
)


router = APIRouter()


@router.post("", response_model=PostOnlyResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    form_data: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await create_post_service(form_data, db, current_user)


@router.get("/feed", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def feed_post(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await feed_post_service(db, current_user)


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(
    post_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_post_service(post_id, db, current_user)


@router.get("", response_model=List[PostOnlyResponse], status_code=status.HTTP_200_OK)
async def my_posts(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await my_posts_service(db, current_user)


@router.patch(
    "/{post_id}", response_model=PostOnlyResponse, status_code=status.HTTP_200_OK
)
async def update_post(
    form_data: PostUpdate,
    post: Annotated[Post, Depends(post_ownership)],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):

    return await update_post_service(post, form_data, db, current_user)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: Annotated[Post, Depends(post_ownership)],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await delete_post_service(post, db, current_user)


@router.delete("/admin/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_admin(
    post_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(required_role(Role.ADMIN))],
):
    await delete_post_admin_service(post_id, db, current_user)
