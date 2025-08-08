from  fastapi  import APIRouter ,Depends
from src.auth.schema import CreateUserModel , UserLoginModel ,UserModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.servises import UserServises
from fastapi.exceptions import HTTPException
from fastapi import status 
from src.db.main import get_session
from src.auth.utils import create_access_token ,verify_password
from  datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from src.auth.dependency import RefreshTokenBearer

auth_router = APIRouter()
user_servises = UserServises()

REFRESH_TOKEN_EXPIRY= 2

@auth_router.post('/signup',response_model=UserModel,status_code=status.HTTP_201_CREATED)
async  def signup(user : CreateUserModel,session : AsyncSession = Depends(get_session)):
    exists_user = await user_servises.user_exists(user.email,session)
    print(exists_user)
    if exists_user  :          
       raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user in the email is already exists')
    new_user =  await user_servises.create_user(user,session) 
    return new_user 
    
@auth_router.post('/login',status_code=status.HTTP_200_OK)
async  def signin(login_data: UserLoginModel ,session : AsyncSession= Depends(get_session)):
   email = login_data.email
   password = login_data.password
   user = await  user_servises.get_user_by_email(email,session)
   if user  is not None :
      password_verify = verify_password(password, user.password_hash)
      
      if password_verify :
         access_token = create_access_token(
            {
               'email' : email,
               'uid' :str( user.uid) ,
            }
         )
         refresh_token = create_access_token(
            user_data={
               'email' : email,
               'uid' :str( user.uid) ,
            },
            expiry= timedelta(days=REFRESH_TOKEN_EXPIRY),
            refresh=True
         )
         return JSONResponse(
           {
            'message' : 'login sucessfully',
            'user' : {
               'uid' : str(user.uid),
               'email' : email
            } ,
            'access' : access_token,
            'refresh' : refresh_token
         }
         )      
   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='crendential does not match')   
         
@auth_router.get('/refresh',status_code=status.HTTP_200_OK)
async  def get_access_token(user_details: dict = Depends(RefreshTokenBearer())):
   print(user_details)
   expairy_timestamp = user_details.get('exp')
   if  datetime.fromtimestamp(expairy_timestamp) > datetime.now() :
      new_access_token= create_access_token(
         user_data= user_details.get('user')
      )
      return {
         'access' : new_access_token
      }
   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid and expiry token')
   
       
         