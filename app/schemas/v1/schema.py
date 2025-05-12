from typing import TYPE_CHECKING
from datetime import datetime
from pydantic import ConfigDict, field_validator

from .base import BaseSkinSchema, BaseUserSchema


if TYPE_CHECKING:
     from app.db.sql.models import Users, Skins





class UserSchema(BaseUserSchema):
     created_at: datetime
     notify: bool
     timer: str | None
     skins: list[BaseSkinSchema]
     
     
     @field_validator("skins")
     @classmethod
     def skins_validator(cls, skins: list["Skins"]) -> list[BaseSkinSchema]:
          if skins:
               return [BaseSkinSchema.model_validate(obj) for obj in skins]
          return []
     
     
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