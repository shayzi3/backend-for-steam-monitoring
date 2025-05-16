from typing import Any
from datetime import timedelta
from pydantic import BaseModel, ConfigDict, model_validator



class Time(BaseModel):
     days: int = 0
     hours: int = 0
     minutes: int = 0
     
     
     @model_validator(mode="after")
     def model_valide(self) -> "Time":
          if (self.days < 0) or (self.hours < 0) or (self.minutes < 0):
               raise ValueError("value for days, hours, minutes must be more than 0")
          
          if self.days > 5:
               raise ValueError("value for days must be less or equal 5")
          
          if self.hours > 24:
               raise ValueError("value for hours must be less or equal 24")
          
          if self.minutes > 60:
               raise ValueError(f"value for minutes must be less or equal 60")
          
          if (self.days == 0) and (self.hours == 0):
               if self.minutes < 25:
                    raise ValueError("value for minutes more or equal 25")
          return self
     
     
     def to_str(self) -> str:
          return f"{self.days}-{self.hours}-{self.minutes}"
     
     
     @classmethod
     def from_str(cls, obj: str) -> "Time":
          """days:hours:minutes"""
          split_obj = obj.strip().split("-")
          if len(split_obj) != 3:
               return "format for time -> days-hours-minutes"
          
          try:
               return cls(
                    days=int(split_obj[0]),
                    hours=int(split_obj[1]),
                    minutes=int(split_obj[2])
               )
          except ValueError as ex:
               return str(ex)
          
          
     def to_timedelta(self) -> timedelta:
          return timedelta(**self.model_dump())
     
     


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
     
     
     