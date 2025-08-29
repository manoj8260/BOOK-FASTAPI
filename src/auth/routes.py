from  fastapi  import APIRouter ,Depends
from src.auth.schema import CreateUserModel , UserLoginModel ,UserModel ,UserBookModel,RegisterModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.servises import UserServises
from fastapi.exceptions import HTTPException
from fastapi import status 
from src.db.main import get_session
from src.auth.utils import create_access_token ,verify_password,encode_url_safe_token,decode_url_safe_token
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from src.auth.dependency import RefreshTokenBearer,AccessTokenBearer ,get_current_user , RoleBasedAccess
from src.auth.redis import blacklist_token 
from src.errors import UserAleradyExists ,UserNotFound
# for send email
from src.auth.schema import EmailModel
from src.mails import mail , send_message
from src.book.config import Config


auth_router = APIRouter()
user_servises = UserServises()
role_access = RoleBasedAccess(['admin','user'])

REFRESH_TOKEN_EXPIRY= 2

@auth_router.post('/send_email')
async def send_email(emails:EmailModel):
   emails = emails.addresses
   html ='<h1> welcome to BOOKly app'
   subject = 'Sucess'
   message = send_message(emails,subject=subject,body=html)
   await mail.send_message(message)
   
   return  {
      "message" : "Email send Sucessfully"
   }


@auth_router.post('/signup',response_model=RegisterModel,status_code=status.HTTP_201_CREATED)
async  def signup(user : CreateUserModel,session : AsyncSession = Depends(get_session)):
    exists_user = await user_servises.user_exists(user.email,session)
    if exists_user  :          
       raise  UserAleradyExists()
    new_user =  await user_servises.create_user(user,session)
    
    token = encode_url_safe_token({'email': new_user.email})
    link=f'http://{Config.DOMAIN}/api/v1/auth/verify/{token}'
    html_message = f"""
        <h1>Verify your Email</h1>
        <p>click this  <a href="{link}">link</a> verify your email</p>
    """ 
    message = send_message(
       recipients=[new_user.email],
       subject='Verify',
       body=html_message
    )
    await mail.send_message(message)
    return {
       'Message' : 'Account created sucessfully ! verify your account ',
       'Hints' : 'Check your Email',
       "User" : new_user
    } 

@auth_router.get('/verify/{token}')
async def  verify_user_account(token:str,session:AsyncSession = Depends(get_session)):
   token_data = decode_url_safe_token(token)
   user_email =token_data.get('email')
   if user_email:
      user = await  user_servises.get_user_by_email(user_email,session)
      if not user :
         raise UserNotFound()
      await user_servises.update_user(user,{'is_active': True},session)
      return JSONResponse(
          content={  'message' : 'Account Verify Sucessfully ! '},
          status_code=status.HTTP_200_OK
      )
   return JSONResponse(
      content={'message' : 'Exception occurs during verifation'},
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
   )   

    
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
async  def get_access_token(token_details: dict = Depends(RefreshTokenBearer())):
   print(token_details)
   expairy_timestamp = token_details.get('exp')
   if  datetime.fromtimestamp(expairy_timestamp) > datetime.now() :
      new_access_token= create_access_token(
         user_data= token_details.get('user')
      )
      return {
         'access' : new_access_token
      }
   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid and expiry token')

@auth_router.get('/me',status_code=status.HTTP_200_OK,response_model=UserBookModel)
async  def current_user(user = Depends(get_current_user), bool  = Depends(role_access)):
   return user    
       
@auth_router.get('/logout')
async  def signout(token_details: dict = Depends(AccessTokenBearer())) :
   jti = token_details['jti']
   await   blacklist_token(jti)
   
   return    JSONResponse(
       {
          'message' : 'Logged out sucessfullt'
       } , status_code= status.HTTP_200_OK
   ) 
