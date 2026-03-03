from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment


async def get_comment_by_id_db(comment_id: UUID, db: AsyncSession):
    stmt = (
        select(Comment)
        .where(Comment.id == comment_id)
        .options(
            selectinload(Comment.author),
            selectinload(Comment.post).options(selectinload(Post.author)),
        )
    )

    result = await db.execute(stmt)
    comment = result.scalars().first()

    return comment


async def create_comment_db(comment: Comment, db: AsyncSession):
    db.add(comment)
    try:
        await db.commit()
        await db.refresh(comment)

    except Exception as e:
        await db.rollback()
        raise e

    return comment


async def get_user_comments_db(
    db: AsyncSession, current_user: User, offset: int, limit: int
):
    stmt = (
        select(Comment)
        .where(Comment.user_id == current_user.id)
        .options(
            selectinload(Comment.author),
            selectinload(Comment.post).options(selectinload(Post.author)),
        )
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(stmt)
    comments = result.scalars().all()

    return comments


async def update_comment_db(to_update: dict, comment: Comment, db: AsyncSession):
    for key, value in to_update.items():
        setattr(comment, key, value)

    try:
        await db.commit()
        await db.refresh(comment)

    except Exception as e:
        await db.rollback()
        raise e

    return comment


async def delete_comment_db(comment: Comment, db: AsyncSession):
    try:
        await db.delete(comment)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise e
