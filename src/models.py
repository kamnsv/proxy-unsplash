from pydantic import BaseModel, BaseSettings, Field


class Photo(BaseModel):
    id: str = ''
    description: str = ''
    image: str = ''


class Raw(BaseModel):
    ...


class Settings(BaseSettings):
    ttl: int = Field('1800', env='TTL_CASH')
    url: str = Field('30', env='URL_API')
    per: int = Field('10', env='PER_PAGE')
    token: str = Field(..., env='TOKEN_API')
    debug: bool = Field('True', env='DEBUG')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
