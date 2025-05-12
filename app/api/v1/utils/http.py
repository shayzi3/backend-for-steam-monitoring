import httpx

from app.response import JsonResponseProtocol
from app.response.error import (
     HttpError,
     HttpStatusCodeError,
     SteamNotFoundItem
)



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
                         return HttpStatusCodeError
                    
                    # 23,32 руб. -> 23.32
                    data = response.json().get("lowest_price")
                    if data is None:
                         return SteamNotFoundItem
                    
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
                    # logging
                    return HttpError
               
               