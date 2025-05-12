from redis.asyncio import Redis

from app.core.config import settings


class RedisSession(Redis):
     def __init__(self) -> None:
          super().__init__(
               host=settings.redis_host,
               port=settings.redis_port
          )