from  fastapi.security  import HTTPBearer 
from fastapi import Request ,status
from src.auth.utils import token_decode
from fastapi.exceptions import HTTPException


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request): 
        credentials = await super().__call__(request)
        token = credentials.credentials
        
        token_data = token_decode(token)
        
        if  not self.is_valid_token(token) :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='token is expiry or invalid')
        
        if  token_data['refresh']  :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='please pass access token')   
        print(token_data)
        # return credentials
        return token_data
    
    def is_valid_token(self,token) :
        decode_token = token_decode(token)
        return True if decode_token is not None  else False
        
        
        