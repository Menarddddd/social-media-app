from uuid import UUID

from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.post import Post
from app.models.user import User


async def get_post_by_id_db(id: UUID, db: AsyncSession):
    stmt = select(Post).where(Post.id == id).options(selectinload(Post.author))
    result = await db.execute(stmt)
    post = result.scalars().first()

    return post


async def create_post_db(post: Post, db: AsyncSession):
    db.add(post)
    try:
        await db.commit()
        await db.refresh(post)

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post",
        )

    return post


async def my_posts_db(current_user: User, db: AsyncSession):
    stmt = select(Post).where(Post.user_id == current_user.id)
    result = await db.execute(stmt)
    posts = result.scalars().all()

    return posts


async def feed_post_db(db: AsyncSession):
    stmt = (
        select(Post)
        .join(Post.author)
        .where(User.deleted_at.is_(None))
        .options(joinedload(Post.author))
    )
    result = await db.execute(stmt)
    posts = result.scalars().all()

    return posts


async def update_post_db(post_data: dict, post: Post, db: AsyncSession):
    for key, value in post_data.items():
        setattr(post, key, value)

    try:
        await db.commit()
        await db.refresh(post)

    except Exception as e:
        await db.rollback()
        raise e

    return post


async def delete_post_db(post: Post, db: AsyncSession):
    try:
        await db.delete(post)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise e
