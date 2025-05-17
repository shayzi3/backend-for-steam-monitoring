import asyncio

from typing import Any
from datetime import datetime

from app.utils.http import HttpClient
from app.response import JsonResponseProtocol
from app.response.error import UserExists, UserNotExists
from app.response.success import UserCreated, UserUpdated
from app.db.sql.repository import UserRepository, SkinRepository
from app.db.redis import RedisSession
from app.schemas.v1 import UserSchema, Time



class UserService:
     def __init__(
          self, 
          user_repository: UserRepository, 
          skin_repository: SkinRepository,
          http_client: HttpClient
     ):
          self.user_repository = user_repository
          self.skin_repository = skin_repository
          self.http_client = http_client
          
          
     async def create_user(
          self,
          telegram_id: int,
          telegram_username: str,
          language: str,
          currency: int
     ) -> JsonResponseProtocol:
          user_exists = await self.user_repository.read(
               redis_value=f"user:{telegram_id}",
               where={"telegram_id": telegram_id},
               redis_write_value=True
          )
          if user_exists is None:
               await self.user_repository.create(
                    values={
                         "telegram_id": telegram_id,
                         "telegram_username": telegram_username,
                         "language": language,
                         "currency": currency,
                         "timer": "0-0-25"
                    }
               )
               return UserCreated
          return UserExists
               
          
     async def get_user(
          self,
          telegram_id: int,
     ) -> UserSchema | JsonResponseProtocol:
          user = await self.user_repository.read(
               redis_value=f"user:{telegram_id}",
               where={"telegram_id": telegram_id} ,
               redis_write_value=True
          )
          if user is None:
               return UserNotExists
          return user
     
     
     async def update_user(
          self,
          telegram_id: int,
          not_nullable_value: dict[str, Any]
     ) -> JsonResponseProtocol:
          update = await self.user_repository.update(
               where={"telegram_id": telegram_id},
               values=not_nullable_value,
               redis_delete_value=[f"user:{telegram_id}"],
          )
          if update is None:
               return UserNotExists
          return UserUpdated

          
          
     async def change_price_of_skins(
          self,
          telegram_id: int
     ) -> None:
          user = await self.user_repository.read(
               redis_value=f"user:{telegram_id}",
               where={"telegram_id": telegram_id},
               redis_write_value=True
          )
          weapon = []
          redis_delete_values = [f"user:{telegram_id}"]
          if user is not None:
               for skin in user.skins:
                    price = await self.http_client.get_price_item(
                         name=skin.name,
                         currency=user.currency
                    )
                    if isinstance(price, float) is False:
                         print(price)
                    
                    weapon.append(
                         {
                             "_telegram_user_id": telegram_id,
                             "_name": skin.name,
                             "_current_price": price
                         }
                    )
                    redis_delete_values.append(f"skin:{skin.skin_id};{telegram_id}")
                    await asyncio.sleep(0.25)
                    
               await self.skin_repository.update_many(
                    data=weapon,
                    redis_delete_values=redis_delete_values
               )
               
             
     async def set_time_in_redis(
          self,
          periodic_time: str,
          telegram_id: int
     ) -> None:
          async with RedisSession() as session:
               time = Time.from_str(periodic_time).to_timedelta()
               new_time = (datetime.now() + time).isoformat()
               
               tasks = [value.decode() for value in await session.lrange("tasks", 0, -1)]
               for index, user in enumerate(tasks):
                    user_id = user.split(":")[-1]
                    if user_id.isdigit():
                         if int(user_id) == telegram_id:
                              return await session.lset(
                                   name="tasks", 
                                   index=index, 
                                   value=f"{periodic_time};{new_time};{telegram_id}"
                              )
               await session.lpush(
                    "tasks", 
                    f"{periodic_time};{new_time};{telegram_id}"
               )
               
     

async def get_user_service() -> UserService:
     return UserService(
          user_repository=UserRepository,
          skin_repository=SkinRepository,
          http_client=HttpClient()
     )