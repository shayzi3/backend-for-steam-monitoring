from typing import Any, Generic
from sqlalchemy import select, update, delete, insert

from app.types import PYDANTIC_MODEL, REDIS_RESULT
from app.db.sql.session import Session
from app.db.redis import RedisSession
from app.schemas.v1 import UserSchema
from app.core.utils import get_currency_curse




class BaseRepository(Generic[PYDANTIC_MODEL]):
     model = None
     
     
     @classmethod
     async def read(
          cls,
          redis_value: str,
          where: dict[str, Any],
          values: list[str] = [],
          redis_result: REDIS_RESULT = "model",
          redis_write_value: bool = True
     ) -> PYDANTIC_MODEL | None:
          async with RedisSession() as session:
               value = await session.get(redis_value)
               if value is not None:
                    if redis_result == "model":
                         return cls.model.__pydantic_model__.model_validate_json(value.decode())
                    return value.decode() # return str or int or dict
               
          async with Session.session() as connection:
               sttm = select(cls.model).filter_by(**where)
               result = await connection.execute(sttm)
               
               scalar = result.scalar() # sqlalchemy model
               if scalar is None:
                    return None
               
          if values:
               return [getattr(scalar, value, None) for value in values]
               
          model = cls.model.__pydantic_model__.model_validate(scalar) 
          if redis_write_value is True:
               async with RedisSession() as session:
                    await session.set(
                         name=redis_value,
                         ex=model.redis_expire,
                         value=model.model_dump_json()
                    )
          return model
                    
          
     @classmethod
     async def create(
          cls,
          values: dict[str, Any],
          redis_delete_value: list[str] = [],
     ) -> None:
          async with Session.session() as connection:
               sttm = insert(cls.model).values(**values)
               await connection.execute(sttm)
               await connection.commit()
               
          if redis_delete_value:
               async with RedisSession() as session:
                    await session.delete(*redis_delete_value)
          
          
     @classmethod
     async def update(
          cls,
          where: dict[str, Any],
          values: dict[str, Any],
          redis_delete_value: list[str] = [],
     ) -> None | bool:
          async with Session.session() as connection:
               sttm = (
                    update(cls.model).
                    filter_by(**where).
                    values(values).
                    returning(cls.model.returning_value())
               )
               result = await connection.execute(sttm)
               await connection.commit()
               
               result = result.fetchone()
               if result is None:
                    return None
          
          if redis_delete_value:
               async with RedisSession() as session:
                    await session.delete(*redis_delete_value)
          return True
               
               
          
     @classmethod
     async def delete(
          cls,
          where: dict[str, Any],
          redis_delete_value: list[str] = [],
     ) -> None:
          async with Session.session() as connection:
               sttm = (
                    delete(cls.model).
                    filter_by(**where).
                    returning(cls.model.returning_value())
               )
               result = await connection.execute(sttm)
               await connection.commit()
               
               result = result.fetchone()
               if result is None:
                    return None
          
          if redis_delete_value:
               async with RedisSession() as session:
                    await session.delete(*redis_delete_value)
          return True