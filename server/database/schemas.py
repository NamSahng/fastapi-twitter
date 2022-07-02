from typing import Union
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username : str
    password : str

class UserCreate(UserBase):
    name : str
    email : str
    url : Union[str, None]
    
class UserOut(BaseModel):
    token : str
    username : str
    class Config:
        orm_mode = True

class isAuthOut(BaseModel):
    Authorization : str
    id : str

class TweetOut(BaseModel):    
    id : int
    text : str
    createdAt : datetime
    userId : str
    name: str
    username : str
    url : Union[str, None]
    class Config:
        orm_mode = True

class TweetNew(BaseModel):
    username : str
    name : str
    text : str

class TweetUpdate(BaseModel):
    text : str
