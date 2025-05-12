from pydantic_settings import BaseSettings, SettingsConfigDict



class Config(BaseSettings):
     postgresql: str
     redis_host: str
     redis_port: int
     
     model_config = SettingsConfigDict(env_file="app/core/.env")
     
     
settings = Config()