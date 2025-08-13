from fastapi import APIRouter ,status,Depends
from typing import List
from fastapi.exceptions import HTTPException
from src.book.book_data import books
from src.book.schema import BookModel,UpdateBook ,CreateBook
from src.db.main import get_session
from src.book.servises import BookServises
from  sqlmodel.ext.asyncio.session import AsyncSession
from .models import Book
from src.auth.dependency import AccessTokenBearer ,RoleBasedAccess


book_router = APIRouter()
book_servise = BookServises()
access_token_bearer = AccessTokenBearer()
role_access = Depends(RoleBasedAccess(['user']))

@book_router.get('/',response_model=List[Book],dependencies=[role_access])
async def all_books(session :AsyncSession = Depends(get_session) , user_details = Depends(access_token_bearer)):
    books = await book_servise.get_books(session)
    print(user_details)
    return  books

@book_router.post('/',response_model=Book)
async def create_book(book : CreateBook ,session :AsyncSession = Depends(get_session),user_details = Depends(access_token_bearer)):
    new_book  =await  book_servise.create_book(book ,session)
    return new_book
    
@book_router.get('/{book_uid}',response_model=Book)
async def get_book(book_uid : str ,session :AsyncSession = Depends(get_session),user_details = Depends(access_token_bearer)):
    book = await book_servise.get_book(book_uid,session)
    if book :
        return book
    else :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book not found')    

@book_router.put('/{book_uid}')
async def update_book(book_uid : str,update_book :UpdateBook,session :AsyncSession = Depends(get_session) , user_details = Depends(access_token_bearer)):
    update_book = await book_servise.update_book(book_uid,update_book,session)
    if update_book :
        return update_book
    else:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found')   

# @book_router.patch('/{book_id}')
# async def update_book(book_id : int ,update_book : UpdateBook,session :AsyncSession = Depends(get_session)):
#     for book in books :
#         if book['id'] == book_id :
#             book['title'] = update_book.title
#             book['author'] = update_book.author
#             return update_book       
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found') 

@book_router.delete('/{book_uid}' ,status_code=status.HTTP_204_NO_CONTENT )
async def delete_book(book_uid : str,session :AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)) :
    book_to_delete = await book_servise.delete_book(book_uid,session)
    if book_to_delete :
        return None
    else :
     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found')     
        
         
            
    