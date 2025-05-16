from typing import Any
from fastapi import BackgroundTasks

from app.schemas.v1 import SkinSchema
from app.response import JsonResponseProtocol
from app.response.success import SkinUpdated, SkinDeleted
from app.response.error import (
     SkinExists,
     UserNotExists,
     SkinNotExists,
)
from app.response.success import SkinCreated
from app.db.sql.repository import SkinRepository, UserRepository
from app.core.security import generate_skin_id
from app.utils.http import HttpClient



class SkinService:
     def __init__(
          self, 
          skin_repository: SkinRepository,
          user_repository: UserRepository,
          http_client: HttpClient
     ):
          self.skin_repository = skin_repository
          self.user_repository = user_repository
          self.http_client = http_client
          self.bg_task = BackgroundTasks()
     
     
     async def get_skin(
          self,
          skin_id: int,
          telegram_id: int
     ) -> SkinSchema | JsonResponseProtocol:
          skin = await self.skin_repository.read(
               redis_value=f"skin:{skin_id};{telegram_id}",
               where={"telegram_user_id": telegram_id, "skin_id": skin_id},
               redis_write_value=True
          )
          if skin is None:
               return SkinNotExists
          return skin
          
          
     async def create_skin(
          self,
          name: str,
          image: str,
          percent: int,
          telegram_id: int
     ) -> JsonResponseProtocol:
          user = await self.user_repository.read(
               redis_value=f"user:{telegram_id}",
               where={"telegram_id": telegram_id},
               redis_write_value=True
          )
          if user is None:
               return UserNotExists
          
          if user.skins:
               for skin in user.skins:
                    if skin.name == name:
                         return SkinExists
          
          price = await self.http_client.get_price_item(
               name=name,
               currency=user.currency
          )
          if isinstance(price, float) is False:
               return price
          
          await self.skin_repository.create(
               values={
                    "skin_id": await generate_skin_id(),
                    "name": name,
                    "image": image,
                    "current_price": price,
                    "percent": percent,
                    "telegram_user_id": telegram_id
               },
               redis_delete_value=[f"user:{telegram_id}"],
          )
          return SkinCreated
          
          
          
     async def change_skin(
          self,
          skin_id: int,
          telegram_id: int,
          non_nullable_values: dict[str, Any]
          ) -> JsonResponseProtocol:
          user_update = await self.skin_repository.update(
               where={"telegram_id": telegram_id, "skin_id": skin_id},
               values=non_nullable_values,
               redis_delete_value=[f"skin:{skin_id};{telegram_id}"],
          )
          if user_update is None:
               return SkinNotExists
          return SkinUpdated
          
          
          
     async def delete_skin(
          self,
          telegram_id: int,
          skin_id: int | None = None,
          skin_name: str | None = None
          ) -> JsonResponseProtocol:
          where = (
               {"skin_id": skin_id}
               if skin_name is None
               else {"name": skin_name}
          )
          where.update({"telegram_id": telegram_id})
          
          user_deleted = await self.skin_repository.delete(
               where=where,
               redis_delete_value=[f"skin:{skin_id};{telegram_id}"],
          )
          if user_deleted is None:
               return SkinNotExists
          return SkinDeleted
          
     
     
     
     
async def get_skin_service() -> SkinService:
     return SkinService(
          skin_repository=SkinRepository,
          user_repository=UserRepository,
          http_client=HttpClient()
     )