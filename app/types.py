from typing import TypeVar, Literal, NewType


REDIS_RESULT = Literal["any", "model"]
PYDANTIC_MODEL = TypeVar("PYDANTIC_MODEL")