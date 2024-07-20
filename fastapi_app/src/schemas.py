from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    """
    User Model
    :param username: str: user name
    :param email: user mail address
    :param password: str: user password
    """
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    User Model in DB
    :param id: int: user id
    :param username: str: username
    :param email: user mail address
    :param role: str: user role : 'admin', 'standard user' or 'modelator'
    :param created_at: datetime: date of user creation
    :param avatar: str: link to user avatar
    """
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    User Response Model
    :param user: UserDB: user data
    :param detail: str: information that the user has been created
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Token Model
    :param access_token: str: user access token
    :param refresh_token: str: user refresh token
    :param token_type: str: type of the token is 'bearer'
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Request Email Model
    : param email: email adress
    """
    email: EmailStr


class Opinion(BaseModel):
    """
    Opinion Model
    :param vote: int : user opinion about the selected image. Accepted only numbers: 1,2,3,4,5 where 1 means the worst image and 5 means the best image.
    :param image_id: the unique image number
    """
    vote: int
    image_id: int