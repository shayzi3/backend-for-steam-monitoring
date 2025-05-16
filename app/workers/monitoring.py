import asyncio

from datetime import datetime
from typing import Any

from app.db.redis import RedisSession
from app.db.sql.repository import UserRepository, SkinRepository
from app.utils.http import HttpClient
from app.schemas.v1 import Time
from app.logs import logging_


class MonitoringWorker:
     def __init__(
          self, 
          user_repository: UserRepository,
          skin_repository: SkinRepository,
          http_client: HttpClient
     ) -> None:
          self.user_repository = user_repository
          self.skin_repository = skin_repository
          self.http_client = http_client
     
     
     async def run(self) -> None:
          while True:
               logging_.worker_monitoring.info("Start worker. Find users by time")
               
               async with RedisSession() as session:
                    tasks = [value.decode() for value in await session.lrange("tasks", 0, -1)]
                    
                    if tasks:
                         parallel = []
                         for index, time_user in enumerate(tasks):
                              period = time_user.split(";")[0]
                              time = datetime.fromisoformat(time_user.split(";")[1])
                              user = int(time_user.split(";")[2])
                              
                              if time <= datetime.now():
                                   new_time = (
                                        datetime.now() + Time.from_str(period).to_timedelta()
                                   ).isoformat()
                                   new_redis_value = f"{period};{new_time};{user}"
                                   await session.lset("tasks", index, new_redis_value)
                                   
                                   logging_.worker_monitoring.info(f"Find user {user} with time {time}")
                                   parallel.append(self.__price_updater(user))
                              
                         if parallel:
                              logging_.worker_monitoring.info("Start gather for users")
                              await asyncio.gather(*parallel)
               await asyncio.sleep(30)
          
          
     async def __price_updater(
          self,
          telegram_id: int
     ) -> None:
          logging_.worker_monitoring.info(f"Start gather for user {telegram_id}")
          
          user = await self.user_repository.read(
               redis_value=f"user:{telegram_id}",
               where={"telegram_id": telegram_id},
               redis_write_value=True
          )
          if (user is None) or (not user.skins) or (user.notify is False):
               return
          
          notify = []
          update_skins = []
          delete_values = [f"user:{telegram_id}"]
          for skin in user.skins:
               new_price = await self.http_client.get_price_item(
                    name=skin.name,
                    currency=user.currency
               )
               if isinstance(new_price, float) is False:
                    continue
               
               max_ = max([skin.current_price, new_price])
               min_ = min([skin.current_price, new_price])
               percent_difference = ((max_ - min_) * 100) // max_
               
               if percent_difference >= skin.percent:
                    logging_.worker_monitoring.info(
                         f"Detect difference persent for {skin.name} at user {telegram_id}"
                    )
                    update_skins.append(
                         {
                              "_telegram_user_id": telegram_id,
                              "_name": skin.name,
                              "_current_price": new_price
                         }
                    )
                    notify.append(
                         {
                              "name": skin.name,
                              "image": skin.image,
                              "last_price": skin.current_price,
                              "update_price": new_price,
                              "difference": percent_difference
                         }
                    )
                    delete_values.append(f"skin:{skin.skin_id};{telegram_id}")
               await asyncio.sleep(1)
               
               
          if update_skins: # if update_skins that and notify 
               logging_.worker_monitoring.info(f"Update skins and send notify for user {telegram_id}")
               
               await self.skin_repository.update_many(
                    data=update_skins,
                    redis_delete_values=delete_values
               )
               await self.__send_notify(
                    data=notify,
                    telegram_id=telegram_id
               )
               
               
     async def __send_notify(
          self,
          data: list[dict[str, Any]],
          telegram_id: int
     ) -> None:
          print(data, telegram_id)