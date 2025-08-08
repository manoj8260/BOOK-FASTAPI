from passlib.context import CryptContext
import jwt
from datetime import timedelta ,datetime
from src.book.config import Config
import uuid
import logging

ACCESS_TOKEN_EXPIRY = 3600

password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str) -> str :
    hash = password_context.hash(password)
    
    return hash
def verify_password(password :str , hash :str) -> bool :
    return password_context.verify(password,hash)

def create_access_token(user_data: dict , expiry : timedelta = None ,refresh : bool =False) -> str:
    payload ={}
    
    payload['user'] = user_data
    payload['exp'] = datetime.now() + ( expiry if expiry  is  not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    
    payload['ixt'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    
    token = jwt.encode(
        payload =payload,
        key= Config.JWT_SECRETKEY,
        algorithm= Config.JWT_ALGORITHM,     
    )
    return token

def token_decode(token : str ) ->dict :
   try :
        token_data =jwt.decode(
         jwt= token ,
         key = Config.JWT_SECRETKEY,
         algorithms= Config.JWT_ALGORITHM
       ) 
        return token_data
   except jwt.PyJWTError as e:
           logging.exception(e)
           return None
        
        