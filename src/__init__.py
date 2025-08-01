from fastapi import FastAPI
from src.book.routes import book_router

version ='v1'
app = FastAPI(
    title= 'BookLy' ,
    description='API end points for book',
    version=version
    
)


app.include_router(book_router,prefix=f'/api/{version}/books' , tags=['Books'])
