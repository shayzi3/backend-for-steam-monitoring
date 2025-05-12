from typing import Any
from pydantic import BaseModel, Field, HttpUrl



class SkinCreateArguments(BaseModel):
     name: str
     image: HttpUrl
     percent: int = Field(le=100, gt=5)
     
     
     
class SkinUpdateArguments(BaseModel):
     current_price: float | None = None
     percent: int | None = Field(default=None, gt=0, le=100)

     
     @property
     def values(self) -> list[str]:
          return list(self.model_dump().values())
     
     
     def non_nullable(self) -> dict[str, Any]:
          return {key: value for key, value in self.model_dump().items() if value is not None}
     
     