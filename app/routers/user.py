from uuid import UUID
from datetime import datetime, timezone
from typing import Annotated, List

from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import Role, User
from app.schemas.user import (
    ChangePasswordRequest,
    PasswordRequest,
    Token,
    UserCreate,
    UserOnlyResponse,
    UserResponse,
    UserUpdate,
)
from app.auth.dependencies import get_current_user, required_role


router = APIRouter()


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
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


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    form_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    data = form_data.model_dump()
    data["password"] = hash_password(data["password"])
    new_user = User(**data)
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user, attribute_names=["posts"])

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist"
        )

    return new_user


@router.get("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.post("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    form_data: ChangePasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
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
    current_user.password = hashed_pwd

    await db.commit()


@router.patch("", response_model=UserOnlyResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    form_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_data = form_data.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(current_user, key, value)

    try:
        await db.commit()
        await db.refresh(current_user)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist"
        )

    return current_user


@router.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    form_data: PasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not verify_password(form_data.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password"
        )

    current_user.deleted_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(current_user)


# ADMIN
@router.get("/admin", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(required_role(Role.ADMIN))],
):
    result = await db.execute(select(User).options(selectinload(User.posts)))
    users = result.scalars().all()

    return users


@router.post("/admin/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(required_role(Role.ADMIN))],
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.deleted_at = datetime.now(timezone.utc)

    await db.commit()


@router.get(
    "/admin/deleted",
    response_model=List[UserOnlyResponse],
    status_code=status.HTTP_200_OK,
)
async def deleted_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(required_role(Role.ADMIN))],
):
    result = await db.execute(select(User).where(User.deleted_at.isnot(None)))
    users = result.scalars().all()

    return users
