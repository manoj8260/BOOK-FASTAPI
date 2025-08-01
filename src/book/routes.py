from fastapi import APIRouter ,status
from typing import List
from fastapi.exceptions import HTTPException
from src.book.book_data import books
from src.book.schema import BookModel,UpdateBook

book_router = APIRouter()

@book_router.get('/',response_model=List[BookModel])
async def all_books():
    return  books

@book_router.post('/',response_model=BookModel)
async def create_book(book : BookModel):
    new_book  = book.model_dump()
    books.append(new_book)
    return new_book
    
@book_router.get('/{book_id}')
async def get_book(book_id : int):
    for book in books:
        if book['id'] == book_id:
            return book
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book not found')    

@book_router.put('/{book_id}')
async def update_book(book_id : int,update_book :BookModel):
    update_book = update_book.model_dump()
    for index , book in enumerate(books) :
        if book['id'] == book_id :
            books[index]= update_book
            return update_book
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found')   

@book_router.patch('/{book_id}')
async def update_book(book_id : int ,update_book : UpdateBook):
    for book in books :
        if book['id'] == book_id :
            book['title'] = update_book.title
            book['author'] = update_book.author
            return update_book       
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found') 

@book_router.delete('/{book_id}' ,status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id : int) :
    for book in books :
        if book['id'] == book_id :
            books.remove(book)   
            return {}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found')     
        
         
            
    