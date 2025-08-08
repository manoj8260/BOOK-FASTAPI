from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
class Settings(BaseSettings):
    DATABASE_URL :str = Field(..., env='DATABASE_URL')
    JWT_SECRETKEY : str = Field(...,env = 'JWT_SECRETKEY')
    JWT_ALGORITHM :str
    
    
    
    model_config = SettingsConfigDict(
        env_file= ".env" ,
        extra="ignore"
    )

Config = Settings()  
