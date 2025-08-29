from  fastapi import APIRouter ,Depends
from src.reviews.schema import CreateReviewModel
from src.auth.dependency import get_current_user
from src.db.main import get_session
from src.db.models import User
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.reviews.servises import ReviewServies

review_router = APIRouter()
review_servise = ReviewServies()


@review_router.post('/book/{book_uid}')
async def create_review(
    book_uid :str,
    review_data : CreateReviewModel,
    user : User = Depends(get_current_user) ,
    session : AsyncSession =  Depends(get_session)
):
    new_review = await review_servise.add_review_to_book(
        user_email= user.email,
        book_uid=book_uid,
        review_data= review_data,
        session=session
    )
    return new_review