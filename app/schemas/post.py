from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str


class PostCreate(PostBase):
    pass


class UserPublic(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class PostOnlyResponse(PostBase):
    id: UUID


class PostResponse(PostBase):
    id: UUID
    author: UserPublic


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
