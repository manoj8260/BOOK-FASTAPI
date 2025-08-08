from  fastapi.security  import HTTPBearer 
from fastapi import Request ,status
from src.auth.utils import token_decode
from fastapi.exceptions import HTTPException


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request): 
        credentials = await super().__call__(request)
        token = credentials.credentials
        
        token_data = token_decode(token)
        
        if  not self.is_valid_token(token) :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='token is expiry or invalid')
        
        self.verify_token_data(token_data)
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
        
            
            