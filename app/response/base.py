from fastapi.responses import JSONResponse

from .abstract_response import JsonResponseProtocol




class BaseJsonResponse(JsonResponseProtocol):
     content: str
     status_code: int
     is_response: bool = True
     
     
     @classmethod
     def response(cls) -> JSONResponse:
          return JSONResponse(
               content={"detail": cls.content},
               status_code=cls.status_code
          )
          
         
          
async def is_response(obj: type) -> bool:
     response = getattr(obj, "is_response", None)
     if response is not True:
          return False
     return True