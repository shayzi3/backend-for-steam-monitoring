from typing import Any
from pydantic import BaseModel

from app.schemas.v1.enums import Language, Currency



class UserCreateArguments(BaseModel):
     telegram_id: int
     telegram_username: str
     language: Language
     currency: Currency
     
     
     def model_post_init(self, _: Any):
          self.language = self.language.value
          self.currency = self.currency.int_value



class UserUpdateArguments(BaseModel):
     language: Language | None = None
     currency: Currency | None = None
     notify: bool | None = None
     timer: str | None = None
     
     
     def model_post_init(self, _: Any):
          if self.language:
               self.language = self.language.value
          
          if self.currency:
               self.currency = self.currency.int_value
               
     
     @property
     def values(self) -> list[Any]:
          return list(self.__dict__.values())
     
     
     def non_nullable(self) -> dict[str, Any]:
          return {
               key: value for key, value in self.__dict__.items() if value is not None
          }