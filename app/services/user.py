from uuid import UUID
from datetime import datetime, timezone

from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user import (
    change_password_db,
    create_user_db,
    delete_user_db,
    deleted_users_db,
    get_user_by_id_db,
    get_user_by_username_db,
    get_users_db,
    update_user_db,
)
from app.schemas.user import (
    ChangePasswordRequest,
    PasswordRequest,
    UserCreate,
    UserUpdate,
)


async def login_service(
    form_data: OAuth2PasswordRequestForm,
    db: AsyncSession,
):
    user = await get_user_by_username_db(form_data.username, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
        )

    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


async def create_user_service(
    form_data: UserCreate,
    db: AsyncSession,
):
    data = form_data.model_dump()
    data["password"] = hash_password(data["password"])
    user = User(**data)

    new_user = await create_user_db(user, db)

    return new_user


# added for scalability
async def profile_service(
    db: AsyncSession,
    current_user: User,
):
    return current_user


async def change_password_service(
    form_data: ChangePasswordRequest,
    db: AsyncSession,
    current_user: User,
):
    if not verify_password(form_data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password change failed",
        )

    if form_data.new_password != form_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New and confirm password must match",
        )

    hashed_pwd = hash_password(form_data.new_password)
    await change_password_db(hashed_pwd, current_user, db)

    return {"message": "Password has been changed successfully."}


async def update_profile_service(
    form_data: UserUpdate,
    db: AsyncSession,
    current_user: User,
):
    user_data = form_data.model_dump(exclude_unset=True)
    updated_user = await update_user_db(user_data, current_user, db)

    return updated_user


async def delete_profile_service(
    form_data: PasswordRequest,
    db: AsyncSession,
    current_user: User,
):
    if not verify_password(form_data.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password"
        )

    current_user.deleted_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(current_user)


# ADMIN
async def get_users_service(
    db: AsyncSession,
    current_user: User,
):
    return await get_users_db(db)


async def delete_user_service(
    user_id: UUID,
    db: AsyncSession,
    current_user: User,
):
    user = await get_user_by_id_db(user_id, db)
    await delete_user_db(user, db)


async def deleted_users_service(
    db: AsyncSession,
    current_user: User,
):
    return await deleted_users_db(db)
