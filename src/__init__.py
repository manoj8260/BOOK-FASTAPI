from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.book.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.errors import register_exception_handlers
from src.middleware import register_middleware

# @asynccontextmanager
# async def life_span(app:FastAPI):
#     print("✅ Starting the server...")
#     await init_db()
#     yield
#     print("🛑 Stopping the server...")



version ='v1'
app = FastAPI(
    title= 'BookLy' ,
    description='A REST API for a book review api  end points ',
    version=version,
    # lifespan=life_span  
    contact={
        'Name' : 'Manoj Kumar nayak',
        'Email' :'mn047653@gmail.com',
        'URL' : 'https://github.com/manoj8260/BOOK-FASTAPI'
    },
    docs_url=f'/api/{version}/docs' ,
    openapi_url=f'/api/{version}/openapi.json',
    redoc_url=f'/api/{version}/redocs',
    
)
register_exception_handlers(app)
register_middleware(app)
   

app.include_router(auth_router,prefix=f'/api/{version}/auth' , tags=['User'])
app.include_router(book_router,prefix=f'/api/{version}/books' , tags=['Books'])
app.include_router(review_router,prefix=f'/api/{version}/reviews' , tags=['Reviews'])

