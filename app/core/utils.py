from app.db.redis import RedisSession
from app.schemas.v1.enums import Currency



async def get_currency_curse(valute: int) -> float:
     str_valute = Currency.from_int_value(valute)
     async with RedisSession() as session:
          float_number = await session.get(str_valute.value)
     return float(float_number.decode())