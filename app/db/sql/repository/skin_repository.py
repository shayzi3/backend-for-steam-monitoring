from typing import Any
from sqlalchemy import update, and_
from sqlalchemy.sql.expression import bindparam

from app.db.redis import RedisSession
from app.db.sql.models import Skins
from app.db.sql.session import Session
from app.schemas.v1 import SkinSchema
from .base import BaseRepository



class SkinRepository(BaseRepository[SkinSchema]):
     model = Skins
     
     
     @classmethod
     async def update_many(
          cls,
          data: list[dict[str, Any]],
          redis_delete_values: list[str] = []
     ) -> None:
          async with Session.engine.begin() as connection:
               sttm = (
                    update(Skins).
                    where(
                         and_(
                              Skins.telegram_user_id == bindparam("_telegram_user_id"),
                              Skins.name == bindparam("_name")
                         )
                    ).
                    values(current_price=bindparam("_current_price"))
               )
               await connection.execute(sttm, data)

          if redis_delete_values:
               async with RedisSession() as session:
                    await session.delete(*redis_delete_values)
               
               