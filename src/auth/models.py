from sqlmodel import SQLModel,Field ,Column 
from sqlalchemy.dialects import postgresql as pg 
import uuid
from datetime import datetime

class User(SQLModel,table = True):
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
    password_hash :str = Field(exclude=True)
    is_active :bool = Field(default=False)
    created_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
    updated_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default =datetime.now()))
     


