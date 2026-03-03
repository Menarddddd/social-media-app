from uuid import UUID
from typing import Annotated, List

from fastapi.routing import APIRouter
from fastapi import Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import comment_ownership, get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.comment import Comment
from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
    CommentWPostResponse,
)
from app.services.comment import (
    create_comment_service,
    delete_comment_admin_service,
    delete_comment_service,
    get_comment_service,
    my_comments_service,
    update_comment_service,
)


router = APIRouter()


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    form_data: CommentCreate,
    post_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await create_comment_service(form_data, post_id, db, current_user)


@router.get(
    "", response_model=List[CommentWPostResponse], status_code=status.HTTP_200_OK
)
async def my_comments(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    page: Annotated[int, Query(ge=1, description="Page number, starts at 1")] = 1,
    limit: Annotated[int, Query(ge=10, le=50, description="Comments per page")] = 10,
):
    return await my_comments_service(db, current_user, page, limit)


@router.get(
    "/{comment_id}", response_model=CommentWPostResponse, status_code=status.HTTP_200_OK
)
async def get_comment(
    comment_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_comment_service(comment_id, db, current_user)


@router.patch(
    "/{comment_id}", response_model=CommentResponse, status_code=status.HTTP_200_OK
)
async def update_comment(
    form_data: CommentUpdate,
    comment: Annotated[Comment, Depends(comment_ownership)],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await update_comment_service(form_data, comment, db, current_user)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment: Annotated[Comment, Depends(comment_ownership)],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await delete_comment_service(comment, db, current_user)


@router.delete("/admin/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_admin(
    comment_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await delete_comment_admin_service(comment_id, db, current_user)
