from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


# ********************
# ****** Users *******
# ********************
class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# ********************
# ****** Posts *******
# ********************
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)


class PostOut(Post):
    votes: int


# ********************
# ****** Vote *******
# ********************


class VoteBase(BaseModel):
    post_id: int
    direction: bool


class Vote(VoteBase):
    pass
