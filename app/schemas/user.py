from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, EmailStr

from app.models.user import Role


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordRequest(BaseModel):
    password: str


class EmailRequest(BaseModel):
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=200)
    new_password: str = Field(min_length=6, max_length=200)
    confirm_password: str = Field(min_length=6, max_length=200)


class UserBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=6, max_length=200)
    email: EmailStr | None = Field(default=None, min_length=6, max_length=200)
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=200)


class UserPublic(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class PostPublic(BaseModel):
    id: UUID
    title: str
    content: str


class CommentPublic(BaseModel):
    id: UUID
    message: str
    author: UserPublic


class UserResponse(UserBase):
    id: UUID


class UserWithPostResponse(UserBase):
    id: UUID

    posts: List[PostPublic]


class UserLoadedResponse(UserBase):
    id: UUID

    posts: List[PostPublic]
    comments: List[CommentPublic]


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None


class PostActivity(BaseModel):
    title: str
    content: str


class CommentActivity(BaseModel):
    message: str


class UserActivityResponse(BaseModel):
    posts: List[PostActivity]
    comments: List[CommentActivity]

    model_config = ConfigDict(from_attributes=True)
