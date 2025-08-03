from pydantic import BaseModel
from datetime import datetime

class BookModel(BaseModel):
        id: int
        title: str
        author: str
        price:int  
        genre: str
        available : bool 
        created_at : datetime
        updated_at : datetime
        
class CreateBook(BaseModel): 
        title: str
        author: str
        price:int  
        genre: str
        available : bool 
        # created_at : datetime
        # updated_at : datetime
          
                

class UpdateBook(BaseModel):
     title: str
     author: str