from  fastapi.security  import HTTPBearer 
from fastapi import Request ,status ,Depends
from src.auth.utils import token_decode
from fastapi.exceptions import HTTPException
from src.auth.redis import is_token_blacklisted
from src.auth.servises import UserServises
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List
from  src.auth.models import User

user_servise = UserServises()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request): 
        credentials = await super().__call__(request)
        token = credentials.credentials
        
        if  not self.is_valid_token(token) :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={'error' : 'token is expairy or envoked','resulation': 'please get a new token' })
        token_data = token_decode(token)
        
        if  await is_token_blacklisted(token_data['jti']):
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={'error' : 'token is expairy or envoked','resulation': 'please get a new token' })
            
        
        self.verify_token_data(token_data)
        print(token_data)
        return token_data
    
    def is_valid_token(self,token) :
        decode_token = token_decode(token)
        return True if decode_token is not None  else False
    
    def verify_token_data(self,token) :
        raise NotImplementedError('please Override the method in child class')
        
        
        
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:str):
         if token_data and  token_data['refresh']  :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='please pass access token')   
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:str):
         if token_data and  not  token_data['refresh']  :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='please pass refresh token')   
        
async  def get_current_user(token_data : dict  = Depends(AccessTokenBearer()) , session :AsyncSession =Depends(get_session) )  :
    email = token_data['user']['email']
    user =  await user_servise.get_user_by_email(email,session)  
    print(user)
    if user : 
       return user
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')         

class RoleBasedAccess:
    def __init__(self,role_access: List[str] )->None :
        self.role_access = role_access
     
    def __call__(self, user : User = Depends(get_current_user)):
        if user.role in self.role_access:
            return True
        else :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you`re not authorised user to access")
                    