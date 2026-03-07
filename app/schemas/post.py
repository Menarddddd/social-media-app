from typing import List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: UUID
    date_created: datetime


class UserPublic(BaseModel):
    first_name: str
    last_name: str


class CommentPublic(BaseModel):
    message: str
    date_created: datetime


class PostFeedResponse(PostBase):
    id: UUID
    date_created: datetime

    author: UserPublic
    comments: List[CommentPublic]


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
