from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import BadRequestException, EntityNotFoundException
from app.models.user import User
from app.models.comment import Comment
from app.repositories.comment import (
    create_comment_db,
    delete_comment_db,
    get_comment_by_id_db,
    get_user_comments_db,
    update_comment_db,
)
from app.repositories.post import get_post_by_id_db
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
)


async def create_comment_service(
    form_data: CommentCreate,
    post_id: UUID,
    db: AsyncSession,
    current_user: User,
):
    post = await get_post_by_id_db(post_id, db)

    if post is None:
        raise EntityNotFoundException("Post", post_id)

    comment_data = form_data.model_dump()

    comment = Comment(**comment_data, post=post, author=current_user)

    new_comment = await create_comment_db(comment, db)

    return new_comment


async def my_comments_service(
    db: AsyncSession, current_user: User, page: int, limit: int
):
    offset = (page - 1) * limit
    comments = await get_user_comments_db(db, current_user, offset, limit)

    return comments


async def get_comment_service(
    comment_id: UUID,
    db: AsyncSession,
    current_user: User,
):
    comment = await get_comment_by_id_db(comment_id, db)

    return comment


async def update_comment_service(
    form_data: CommentUpdate,
    comment: Comment,
    db: AsyncSession,
    current_user: User,
):
    to_update = form_data.model_dump()

    updated_comment = await update_comment_db(to_update, comment, db)

    return updated_comment


async def delete_comment_service(
    comment: Comment,
    db: AsyncSession,
    current_user: User,
):
    try:
        await delete_comment_db(comment, db)

    except:
        raise BadRequestException("Delete post failed")


async def delete_comment_admin_service(
    comment_id: UUID,
    db: AsyncSession,
    current_user: User,
):
    comment = await get_comment_by_id_db(comment_id, db)
    if comment is None:
        raise EntityNotFoundException("Comment", comment_id)

    try:
        await delete_comment_db(comment, db)

    except:
        raise BadRequestException("Delete post failed")
