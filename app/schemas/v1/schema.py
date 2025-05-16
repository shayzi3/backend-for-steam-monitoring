from typing import TYPE_CHECKING
from datetime import datetime
from pydantic import field_validator, Field

from .base import BaseSkinSchema, BaseUserSchema, Time


if TYPE_CHECKING:
     from app.db.sql.models import Users, Skins





class UserSchema(BaseUserSchema):
     created_at: datetime
     notify: bool
     timer: Time | str # in this attribute keeping only Time
     skins: list[BaseSkinSchema]
     
     
     @field_validator("skins")
     @classmethod
     def skins_validator(cls, skins: list["Skins"]) -> list[BaseSkinSchema]:
          if skins:
               return [BaseSkinSchema.model_validate(obj) for obj in skins]
          return []
     
     
     @field_validator("timer")
     @classmethod
     def timer_validator(cls, timer: str | dict):
          # dict comes from redis
          if isinstance(timer, str):
               return Time.from_str(timer)
          return timer
     
     
     @property
     def redis_value(self) -> str:
          return f"user:{self.telegram_id}"
     
     
     
     
class SkinSchema(BaseSkinSchema):
     user: BaseUserSchema
     
     
     @field_validator("user")
     @classmethod
     def user_validator(cls, user: "Users") -> BaseUserSchema:
          return BaseUserSchema.model_validate(user)
     

     @property
     def redis_value(self) -> str:
          return f"skin:{self.name};{self.user.telegram_id}"