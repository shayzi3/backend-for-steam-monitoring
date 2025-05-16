from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, func, ForeignKey


from app.schemas.v1 import UserSchema, SkinSchema
from .base import Base



class Users(Base):
     __pydantic_model__ = UserSchema
     __tablename__ = "users"
     
     telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     telegram_username: Mapped[str] = mapped_column(nullable=False)
     language: Mapped[str] = mapped_column(nullable=False)
     currency: Mapped[int] = mapped_column(nullable=False)
     created_at: Mapped[datetime] = mapped_column(default=func.now())
     notify: Mapped[bool] = mapped_column(default=False)
     timer: Mapped[str] = mapped_column(nullable=True)
     is_admin: Mapped[bool] = mapped_column(default=False)
     
     skins: Mapped[list["Skins"]] = relationship(
          back_populates="user",
          uselist=True,
          lazy="joined"
     )
     
     @classmethod
     def returning_value(cls):
          return cls.telegram_id
     
     
     def __str__(self):
          return "Users"     
     
     
class Skins(Base):
     __pydantic_model__ = SkinSchema
     __tablename__ = "skins"
     
     skin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     name: Mapped[str] = mapped_column(nullable=False)
     image: Mapped[str] = mapped_column(nullable=False)
     current_price: Mapped[float] = mapped_column(nullable=False)
     percent: Mapped[int] = mapped_column(nullable=True)
     telegram_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
     
     user: Mapped["Users"] = relationship(
          back_populates="skins",
          lazy="joined"
     )
     
     @classmethod
     def returning_value(cls):
          return cls.skin_id
     
     def __str__(self):
          return "Skins"
     