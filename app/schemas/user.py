from uuid import UUID
from typing import List
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class DeleteProfile(BaseModel):
    password: str
    reason: str | None = None


class UserBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=6, max_length=200)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=200)


class UserResponse(UserBase):
    id: UUID


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
