from  sqlalchemy.ext.asyncio.session import AsyncSession
from src.book.servises import   BookServises
from src.auth.servises import UserServises
from src.reviews.schema import CreateReviewModel
from src.db.models import Review
from fastapi.exceptions import HTTPException 
from fastapi import status

book_servises = BookServises()
user_servises = UserServises()

class  ReviewServies:
    async def add_review_to_book(self,user_email : str ,book_uid :str,review_data : CreateReviewModel, session :AsyncSession ):
      try :
            user = await user_servises.get_user_by_email(user_email,session)
            book = await book_servises.get_book(book_uid=book_uid,session=session)
            review_data_dict = review_data.model_dump()
            new_review =Review(
               **review_data_dict
            )
            new_review.user = user
            new_review.book = book
            
            session.add(new_review)
            await  session.commit()
            await session.refresh(new_review)
            
            return new_review           
      except  Exception  as e :
            raise  HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f'oops... somethig went to wrong : {e}'
                ) 
        