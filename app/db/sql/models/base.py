from typing import Any

from sqlalchemy.orm import DeclarativeBase




class Base(DeclarativeBase):
     __pydantic_model__: Any