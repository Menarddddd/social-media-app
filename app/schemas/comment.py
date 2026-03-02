from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    message: str = Field(min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: UUID
    created_at: datetime


class UserPublic(BaseModel):
    first_name: str
    last_name: str


class PostPublic(BaseModel):
    title: str
    content: str
    created_at: datetime
    author: UserPublic


class CommentWPostResponse(CommentBase):
    id: UUID
    created_at: datetime
    post: PostPublic


class CommentWUserResponse(CommentBase):
    id: UUID
    created_at: datetime
    author: UserPublic


class CommentUpdate(BaseModel):
    message: str | None = None
