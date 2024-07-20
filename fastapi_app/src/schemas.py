from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    photo_id: int

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    url: str
    description: Optional[str] = None


class PhotoCreate(PhotoBase):
    pass


class Photo(PhotoBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PhotoSearch(BaseModel):
    keywords: Optional[str] = None
    tags: Optional[List[str]] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class UserPhotoSearch(PhotoSearch):
    user_id: Optional[int] = None