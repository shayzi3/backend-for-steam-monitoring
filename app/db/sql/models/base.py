from typing import Generic

from sqlalchemy.orm import DeclarativeBase

from app.types import PYDANTIC_MODEL



class Base(DeclarativeBase, Generic[PYDANTIC_MODEL]):
     __pydantic_model__: PYDANTIC_MODEL
     