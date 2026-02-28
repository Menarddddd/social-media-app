from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, EmailStr

from app.models.user import Role


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordRequest(BaseModel):
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=200)
    new_password: str = Field(min_length=6, max_length=200)
    confirm_password: str = Field(min_length=6, max_length=200)


class UserBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=6, max_length=200)
    email: EmailStr = Field(min_length=6, max_length=200)
    role: Role


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=200)


class PostPublic(BaseModel):
    id: UUID
    title: str
    content: str


class UserOnlyResponse(UserBase):
    id: UUID
    password: str


class UserResponse(UserBase):
    id: UUID
    password: str
    deleted_at: datetime | None

    posts: List[PostPublic]

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
