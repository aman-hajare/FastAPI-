from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# this is schema or pydentic Model parent class what respone get user or which define structure of a request and response (the ensure user create post go through if "title" and content in body show only content and body here rsponse model  Post inherit by PostBase) 
class PostBase(BaseModel): #its help and ensure define model data, format
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel): # here not use parent class use direct BaseModel cause we want to not show email and passwoed
    id: int
    email: EmailStr
    create_at: datetime
    ###Respons model
    model_config = ConfigDict(from_attributes=True) # its response model ,output
    # class Config: # its response model ,output
    #     from_attributes = True
#this define what response gone to the user (request/reponse) id create_at and also title content published cause its Inheritenc by PostBase with follow order without this unorder response
class Post(PostBase):
    id: int
    create_at: datetime # its response model output
    owner_id: int
    owner: UserOut

    ###Respons model
    model_config = ConfigDict(from_attributes=True) # its response model ,output
    # class Config: # its allow to Post class or any class for response model add on path(define just above and inside to class)
    #     from_attributes = True  

class PostOut(BaseModel):
    Post: Post # post have all and PostOut have votes
    votes: int
    model_config = ConfigDict(from_attributes=True) # its response model ,output
    # class Config:
    #     from_attributes = True


class UserCreate(BaseModel): #its help to define  model data ,format
    email: EmailStr  # its module for valid email(Str to EmailStr)
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: bool # True=1 =add vote, False=0= already vote

