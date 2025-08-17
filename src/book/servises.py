from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import  select ,desc
from src.db.models import Book
from src.book.schema import CreateBook ,UpdateBook


class BookServises:
    async def get_books(self,session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        
        return result.all()
    async def get_user_books(self,user_uid:str,session:AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        
        return result.all()
    async def get_book(self,book_uid  : str ,session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book  = result.first()
        return  book if book is not None else None 
    async  def create_book(self,create_book : CreateBook ,user_uid :str, session : AsyncSession):
        book_data = create_book.model_dump()
        
        new_book = Book(**book_data)
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        return  new_book
    
    async def update_book(self,book_uid : str , update_book : UpdateBook ,session : AsyncSession):
        get_update_book = await self.get_book(book_uid,session)
        
        if get_update_book is not None :
            update_book_data = update_book.model_dump()
        
            for key ,value in update_book_data.items():
               setattr(get_update_book,key,value)
            
            await session.commit()
            return get_update_book
        else:
          return None
    async def delete_book(self,book_uid :str,session : AsyncSession):
        book_to_delete= await self.get_book(book_uid,session)
        if  book_to_delete is not None :
              await session.delete(book_to_delete)
              
              await session.commit()
              return {}
        else :
            return None      
       
              
            
        
        