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

class CommentBase(BaseModel):
    """
    Commend Base Model
    :param content: str: comment to the photo
    """
    content: str


class CommentCreate(CommentBase):
    """
    Comment Create Model
    """
    pass


class CommentUpdate(CommentBase):
    """
    Comment Update Model
    """
    pass


class Comment(CommentBase):
    """
    Comment Model
    :param id: int: comment id number
    :param created_at: date and time of comment creation
    :para updated_at: date and time the comment was updated
    :param user_id: int: user id
    :param photo_id: int: photo id
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    photo_id: int

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    """
    Photo Base Model
    :param url: str: ulr adress to the photo
    :param description: description of the selected photo
    :param tags: tags associated with the selected image
    """
    url: str
    description: Optional[str] = None
    tags: Optional[str]


class PhotoCreate(PhotoBase):
    """
    Photo Create Model
    """
    pass


class Photo(PhotoBase):
    """
    Photo Model
    :param id: int: photo's id numeber
    :param user_id: int: user id number
    :param created_at: date and time of photo's creation 
    """
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PhotoSearch(BaseModel):
    """
    Photo Search Model: 
    """
    keywords: Optional[str] = None
    tags: Optional[List[str]] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class UserSearch(BaseModel):
    """
    User Search Model
    :param user_id: int: user's id
    """
    user_id: int


class ProfileResponse(BaseModel):
    """
    Profile Response Model
    :param username: str: username
    :para email: user's email addres
    :param role: str: the role of the user: administrator, standard user or modelator
    :param avatar: str: link to the user's avatar 
    :param photo_amount: int: number of images for a selected user
    """
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    avatar: str
    photo_amount: int

    class Config:
        orm_mode = True

class ProfileStatusUpdate(BaseModel):
    """
    Profile Status Update Model
    :param username: str: username
    :param password: : str: password of the user
    :param avatar: str: link to the user's avatar 
     """
    username: str
    password: str
    avatar: str