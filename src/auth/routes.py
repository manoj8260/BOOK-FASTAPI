from  fastapi  import APIRouter ,Depends
from src.auth.schema import CreateUserModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.servises import UserServises
from fastapi.exceptions import HTTPException
from fastapi import status 
from src.db.main import get_session
from  src.auth.schema import UserModel

auth_router = APIRouter()
user_servises = UserServises()


@auth_router.post('/signup',response_model=UserModel,status_code=status.HTTP_201_CREATED)
async  def signup(user : CreateUserModel,session : AsyncSession = Depends(get_session)):
    exists_user = await user_servises.user_exists(user.email,session)
    print(exists_user)
    if exists_user  :          
       raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user in the email is already exists')
    new_user =  await user_servises.create_user(user,session) 
    return new_user 
    
    
         