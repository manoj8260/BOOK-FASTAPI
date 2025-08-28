from pydantic import BaseModel ,Field
from  datetime import datetime
import uuid
from typing import List
from src.db.models import Book

class EmailModel(BaseModel):
    addresses : List[str]

class CreateUserModel(BaseModel):
    first_name : str = Field(min_length=5)
    last_name : str  = Field(min_length=5)
    username :str = Field(max_length=6)
    email : str   = Field(min_length=5 ,max_length=50)
    password :str  
    
class UserModel(BaseModel) :
    uid : uuid.UUID 
    username :str
    email :str 
    first_name : str
    last_name : str 
    password_hash :str = Field(exclude=True)
    is_active :bool 
    created_at : datetime
    updated_at : datetime  
    
class UserBookModel(UserModel):     
    books :List[Book]  

class UserLoginModel(BaseModel):
    email : str 
    password : str     