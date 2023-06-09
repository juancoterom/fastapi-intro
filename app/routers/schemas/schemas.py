from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    votes: int
    created_at: datetime
    owner: UserResponse

    class Config:
        orm_mode = True


class VoteBase(BaseModel):
    post_id: int


class VoteCreate(VoteBase):
    pass