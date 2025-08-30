from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
class Settings(BaseSettings):
    DATABASE_URL :str = Field(..., env='DATABASE_URL')
    JWT_SECRETKEY : str = Field(...,env = 'JWT_SECRETKEY')
    JWT_ALGORITHM :str
    REDIS_HOST : str = 'localhost'
    REDIS_PORT : int = 6379
    REDIS_URL :str = 'redis://localhost:6379/0'
    DOMAIN : str 
    
    MAIL_USERNAME :str
    MAIL_SERVER :str 
    MAIL_PASSWORD  :str
    MAIL_FROM :str
    MAIL_FROM_NAME  :str
    MAIL_PORT :int 
    MAIL_STARTTLS :bool = True
    MAIL_SSL_TLS : bool = False
    USE_CREDENTIALS :bool = True
    VALIDATE_CERTS : bool =True
    
    
    
    model_config = SettingsConfigDict(
        env_file= ".env" ,
        extra="ignore"
    )

Config = Settings()  

broker_url =Config.REDIS_URL
result_backend = Config.REDIS_URL
