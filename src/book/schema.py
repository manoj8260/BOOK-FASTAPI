from pydantic import BaseModel

class BookModel(BaseModel):
        id: int
        title: str
        author: str
        price:int  
        genre: str
        available : bool 

class UpdateBook(BaseModel):
     title: str
     author: str