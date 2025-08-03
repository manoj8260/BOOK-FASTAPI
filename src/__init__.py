from fastapi import FastAPI
from src.book.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
@asynccontextmanager
async def life_span(app:FastAPI):
    print("✅ Starting the server...")
    await init_db()
    yield
    print("🛑 Stopping the server...")



version ='v1'
app = FastAPI(
    title= 'BookLy' ,
    description='API end points for book',
    version=version,
    lifespan=life_span
    
)


app.include_router(book_router,prefix=f'/api/{version}/books' , tags=['Books'])
