from  sqlmodel import SQLModel ,Field,Column ,ForeignKey ,Relationship
from sqlalchemy.dialects import postgresql as pg
from datetime import datetime
import uuid
from typing import Optional ,List


class User(SQLModel,table = True):
    __tablename__ ='users'
    uid : uuid.UUID = Field(
            sa_column=Column(
                pg.UUID,
                primary_key=True,
                nullable=False,
                default=uuid.uuid4
            )
        )
    username :str
    email :str 
    first_name : str
    last_name : str 
    role :str = Field(sa_column=Column(pg.VARCHAR,server_default='user',nullable=False))
    password_hash :str = Field(exclude=True)
    is_active :bool = Field(default=False)
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
    updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
    books : List['Book'] = Relationship(back_populates='user' ,sa_relationship_kwargs={"lazy": "selectin"})
    reviews : Optional['Review'] = Relationship(back_populates='user',sa_relationship_kwargs={"lazy": "selectin"})
    

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
        
        user_uid : uuid.UUID = Field(sa_column=Column(pg.UUID,ForeignKey("users.uid", ondelete="CASCADE") ,nullable=False))
        user : Optional[User] = Relationship(back_populates='books')
        reviews : Optional['Review'] =  Relationship(back_populates='book')
        
        def __repr__(self):
                return f"<Book {self.title}"



     
         
class Review(SQLModel,table = True):
    __tablename__ ='reviews'
    uid : uuid.UUID = Field(
            sa_column=Column(
                pg.UUID,
                primary_key=True,
                nullable=False,
                default=uuid.uuid4
            )
        )
    review_text : str 
    rating : int =Field(lt= 5)
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
    updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
    user_uid : Optional[uuid.UUID] = Field(sa_column=Column(pg.UUID,ForeignKey("users.uid", ondelete="CASCADE") ,nullable=True))
    book_uid : Optional[uuid.UUID] = Field(sa_column=Column(pg.UUID,ForeignKey("books.uid", ondelete="CASCADE") ,nullable=True))
    user : Optional[User] = Relationship(back_populates='reviews')
    book : Optional[Book] = Relationship(back_populates='reviews')
     
         