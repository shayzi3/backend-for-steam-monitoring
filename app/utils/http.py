from typing import Any
import httpx

from app.response import JsonResponseProtocol
from app.response.error import (
     HttpError,
     HttpStatusCodeError,
     SteamNotFoundItem
)
from app.logs import logging_
from app.core.config import settings



class HttpClient:
     def __init__(self):
          self.price_search_url = (
               "https://steamcommunity.com/market/"
               "priceoverview/?currency=currency_&appid=730&market_hash_name=market_name_"
          )
          
          
     async def price_url_builder(
          self,
          name: str,
          currency: int
     ) -> str:
          url = self.price_search_url.replace("currency_", str(currency))
          url = url.replace("market_name_", name)
          return url
     
     
     async def get_price_item(
          self, 
          name: str,
          currency: int
     ) -> float | JsonResponseProtocol:
          url = await self.price_url_builder(name, currency)
          async with httpx.AsyncClient() as session:
               try:
                    response = await session.get(url=url)
                    
                    if response.status_code != 200:
                         logging_.http.error(f"STEAM STATUS CODE ERROR: {response.text}")
                         return HttpStatusCodeError
                    
                    # 23,32 руб. -> 23.32
                    data = response.json().get("lowest_price")
                    if data is None:
                         logging_.http.error(f"STEAM NOT FOUND ITEM: {name}")
                         return SteamNotFoundItem
                    
                    logging_.http.info(f"STEAM SUCCESS FIND ITEM: {name}")
                    
                    if currency == 1: # dollar
                         # $119.17 -> 119.17
                         return float(data[1:])
                    
                    elif currency == 5: # rub
                         # 9978,68 руб. -> 9978.68
                         return float(data.replace(",", ".").split()[0])
                    
                    elif (currency == 18) or (currency == 3): # eur or uah
                         # 4 957,16₴ -> 4957.16
                         return float(data.replace(",", ".").replace(" ", "")[:-1])
               
               
               except Exception as ex:
                    logging_.http.error(exc_info=ex, msg="error")
                    return HttpError
               
               
     async def send_notify_message(
          self,
          data: list[dict[str, Any]],
          telegram_id: int
     ) -> None:
          url = (
               settings.bot_webhook_url 
               + "/webhook/notify" 
               + f"?telegram_id={telegram_id}"
          )
          async with httpx.AsyncClient() as session:
               try_ = 0
               json = {"skins": data}
               while try_ < 3:
                    response = await session.post(url=url, json=json)
                    
                    if response.status_code == 200:
                         logging_.http.info(f"Send notify for user {telegram_id} success")
                         return None
                    try_ += 1
               logging_.http.error(f"Error to send notify for user {telegram_id}")
                    
                    
     async def send_exception_message(
          self,
          exec: str
     ) -> None:
          url = (
               settings.bot_webhook_url
               + "/webhook/exception"
               + f"?exec={exec}"
          )
          async with httpx.AsyncClient() as session:
               try_ = 0 
               while try_ < 3:
                    response = await session.post(url=url)
                    
                    if response.status_code == 200:
                         logging_.http.info("Success")
                         return None
                    try_ += 1
               logging_.http.error("Error to send exception")
                    
               
               