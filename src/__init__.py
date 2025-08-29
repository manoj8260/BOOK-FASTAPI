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
    description='API end points for book',
    version=version,
    # lifespan=life_span   
)
register_exception_handlers(app)
register_middleware(app)
   

app.include_router(auth_router,prefix=f'/api/{version}/auth' , tags=['User'])
app.include_router(book_router,prefix=f'/api/{version}/books' , tags=['Books'])
app.include_router(review_router,prefix=f'/api/{version}/reviews' , tags=['Reviews'])

