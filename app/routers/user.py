from uuid import UUID
from typing import Annotated, List

from fastapi.routing import APIRouter
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
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
from app.core.dependencies import get_current_user, required_role
from app.services.user import (
    change_password_service,
    create_user_service,
    delete_profile_service,
    delete_user_service,
    deleted_users_service,
    get_user_service,
    get_users_service,
    login_service,
    profile_service,
    update_profile_service,
)


router = APIRouter()


# ADMIN
@router.get("/admin", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(required_role(Role.ADMIN))],
):
    return await get_users_service(db, current_user)


@router.delete("/admin/{user_Id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(required_role(Role.ADMIN))],
):
    await delete_user_service(user_id, db, current_user)


@router.get(
    "/admin/deleted",
    response_model=List[UserOnlyResponse],
    status_code=status.HTTP_200_OK,
)
async def deleted_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(required_role(Role.ADMIN))],
):
    return await deleted_users_service(db, current_user)


# USER
@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await login_service(form_data, db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    form_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await create_user_service(form_data, db)


@router.get("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await profile_service(db, current_user)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_user_service(user_id, db, current_user)


@router.post("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
    form_data: ChangePasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await change_password_service(form_data, db, current_user)


@router.patch("", response_model=UserOnlyResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    form_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await update_profile_service(form_data, db, current_user)


@router.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    form_data: PasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await delete_profile_service(form_data, db, current_user)
