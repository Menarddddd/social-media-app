from typing import List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str

    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    pass


class UserPublic(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class PostOnlyResponse(PostBase):
    id: UUID
    created_at: datetime


class PostResponse(PostBase):
    id: UUID
    author: UserPublic
    created_at: datetime


class CommentPublic(BaseModel):
    id: UUID
    message: str
    created_at: datetime
    author: UserPublic


class PostWCommentResponse(PostBase):
    id: UUID
    author: UserPublic
    created_at: datetime
    comments: List[CommentPublic]


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
