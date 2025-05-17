from typing import Protocol
from fastapi.responses import JSONResponse



class JsonResponseProtocol(Protocol):
     content: str
     status_code: int
     
     @classmethod
     def response(cls) -> JSONResponse:
          ...