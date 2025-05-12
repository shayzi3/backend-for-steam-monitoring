from typing import Any
from pydantic import BaseModel, ConfigDict





class BaseSkinSchema(BaseModel):
     skin_id: int
     name: str
     image: str
     current_price: float
     percent: int
     
     model_config = ConfigDict(from_attributes=True)
     
     
     @property
     def redis_expire(self) -> int:
          return 300
     
     
     def to_redis(self) -> dict[str, Any]:
          return self.__dict__
     
     
     
     
     
class BaseUserSchema(BaseModel):
     telegram_id: int
     telegram_username: str
     language: str
     currency: int
     is_admin: bool
     
     model_config = ConfigDict(from_attributes=True)
     
     
     @property
     def redis_expire(self) -> int:
          return 600
     
     
     def to_redis(self) -> dict[str, Any]:
          return self.__dict__
     
     
     