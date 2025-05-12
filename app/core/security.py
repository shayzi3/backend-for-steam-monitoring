import random

from string import digits
from app.db.redis import RedisSession



async def verify_token(token: str, service: str) -> bool:
     async with RedisSession() as session:
          get_token = await session.get(name=service)
     
     if token == get_token.decode("utf-8"):
          return True
     return False


async def generate_skin_id() -> int:
     return int("".join([random.choice(digits) for _ in range(10)]))
