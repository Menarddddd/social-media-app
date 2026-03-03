from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.comment import Comment


# ADMIN
async def get_users_db(db: AsyncSession):
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.posts),
            selectinload(User.comments).options(selectinload(Comment.author)),
        )
        .where(User.deleted_at.is_(None))
    )
    users = result.scalars().all()

    return users


async def deleted_users_db(db: AsyncSession):
    result = await db.execute(select(User).where(User.deleted_at.isnot(None)))
    users = result.scalars().all()

    return users


# FETCH
async def _get_user_db(filter_condition, db: AsyncSession):
    stmt = (
        select(User)
        .options(
            selectinload(User.posts),
            selectinload(User.comments).options(selectinload(Comment.author)),
        )
        .where(filter_condition, User.deleted_at.is_(None))
    )

    result = await db.execute(stmt)
    user = result.scalars().first()

    return user


async def get_user_by_id_db(id: UUID, db: AsyncSession):
    return await _get_user_db(User.id == id, db)


async def get_user_by_username_db(username: str, db: AsyncSession):
    return await _get_user_db(User.username == username, db)


async def get_user_by_email_db(email: str, db: AsyncSession):
    return await _get_user_db(User.email == email, db)


# CREATE
async def create_user_db(user: User, db: AsyncSession):
    db.add(user)

    try:
        await db.commit()
        await db.refresh(user, attribute_names=["posts", "comments"])

    except IntegrityError as e:
        await db.rollback()
        raise e

    return user


# UPDATE
async def update_user_db(user_data: dict, user: User, db: AsyncSession):
    for key, value in user_data.items():
        setattr(user, key, value)

    try:
        await db.commit()
        await db.refresh(user)

    except IntegrityError as e:
        await db.rollback()
        raise e

    return user


async def change_password_db(hashed_pwd: str, user: User, db: AsyncSession):
    user.password = hashed_pwd
    await db.commit()


async def set_email_db(email: str, user: User, db: AsyncSession):
    try:
        user.email = email
        await db.commit()

    except IntegrityError as e:
        await db.rollback()
        raise e


# DELETE
async def delete_user_db(user: User, db: AsyncSession):
    user.deleted_at = datetime.now(timezone.utc)
    await db.commit()
