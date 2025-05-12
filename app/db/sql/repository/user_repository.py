from app.schemas.v1 import UserSchema
from app.db.sql.models import Users
from .base import BaseRepository



class UserRepository(BaseRepository[UserSchema]):
     model = Users