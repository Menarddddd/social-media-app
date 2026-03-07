from typing import List, Any
from uuid import UUID
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.models.user import User


async def feed_post_db(
    db: AsyncSession, offset: int, limit: int, *options
) -> List[Post]:
    stmt = select(Post).order_by(Post.date_created.desc()).offset(offset).limit(limit)
    if options:
        stmt = stmt.options(*options)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_post_by_id_db(post_id: UUID, db: AsyncSession, *options) -> Post | None:
    stmt = select(Post).where(Post.id == post_id)
    if options:
        stmt = stmt.options(*options)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_user_post_db(
    db: AsyncSession, user: User, offset, limit
) -> List[Post]:
    stmt = select(Post).where(Post.user_id == user.id).offset(offset).limit(limit)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def limit_post_db(
    user_id: UUID, db: AsyncSession, offset: int, limit: int, *options
) -> List[Post]:
    stmt = select(Post).where(Post.user_id == user_id).offset(offset).limit(limit)

    if options:
        stmt = stmt.options(*options)

    result = await db.execute(stmt)
    posts = result.scalars().all()

    return list(posts)


async def add_post_db(post: Post, db: AsyncSession) -> Post:
    db.add(post)
    await db.flush()

    return post


async def delete_post_db(post: Post, db: AsyncSession) -> None:
    await db.delete(post)
    await db.flush()
