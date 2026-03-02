from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import (
    EntityNotFoundException,
    UnprocessableException,
)
from app.models.post import Post
from app.models.user import User
from app.repositories.post import (
    create_post_db,
    delete_post_db,
    feed_post_db,
    get_post_by_id_db,
    my_posts_db,
    update_post_db,
)
from app.schemas.post import PostCreate, PostUpdate


async def create_post_service(
    form_data: PostCreate,
    db: AsyncSession,
    current_user: User,
):
    post = Post(**form_data.model_dump(), author=current_user)
    new_post = await create_post_db(post, db)

    return new_post


async def feed_post_service(
    db: AsyncSession,
    current_user: User,
):
    return await feed_post_db(db)


async def get_post_service(post_id: UUID, db: AsyncSession, current_user: User):
    post = await get_post_by_id_db(post_id, db)
    if not post:
        raise EntityNotFoundException("Post", post_id)

    return post


async def my_posts_service(
    db: AsyncSession,
    current_user: User,
):
    return await my_posts_db(current_user, db)


async def update_post_service(
    post: Post,
    form_data: PostUpdate,
    db: AsyncSession,
    current_user: User,
):
    to_update = form_data.model_dump(exclude_unset=True)

    try:
        updated_post = await update_post_db(to_update, post, db)

    except Exception as e:
        raise UnprocessableException("Post update failed")

    return updated_post


async def delete_post_service(
    post: Post,
    db: AsyncSession,
    current_user: User,
):
    try:
        await delete_post_db(post, db)

    except Exception as e:
        raise UnprocessableException("Delete post failed")


async def delete_post_admin_service(
    post_id: UUID,
    db: AsyncSession,
    current_user: User,
):
    post = await get_post_by_id_db(post_id, db)
    if post is None:
        raise EntityNotFoundException("Post", post_id)

    await delete_post_db(post, db)
