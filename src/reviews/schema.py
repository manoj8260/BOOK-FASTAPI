from pydantic import BaseModel ,Field
from datetime import datetime
import uuid
from typing import Optional
class ReviewModel(BaseModel):
    uid : uuid.UUID 
    review_text : str 
    rating : int 
    created_at : datetime 
    updated_at : datetime  
    user_uid : Optional[uuid.UUID] 
    book_uid : Optional[uuid.UUID] 
    
     
         

class CreateReviewModel(BaseModel):
    review_text : str 
    rating : int = Field(lt= 5)