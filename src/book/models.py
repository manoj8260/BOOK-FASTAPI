from  sqlmodel import SQLModel ,Field,Column
from sqlalchemy.dialects import postgresql as pg
from datetime import datetime
import uuid


class Book(SQLModel,table= True):
        __tablename__ = 'books'
        uid: uuid.UUID  = Field(
            sa_column=Column(
                pg.UUID,
                primary_key=True,
                nullable=False,
                default=uuid.uuid4
            )
        )
        title: str
        author: str
        price:int  
        genre: str
        available : bool 
        created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
        updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
        
        def __repr__(self):
                return f"<Book {self.title}"