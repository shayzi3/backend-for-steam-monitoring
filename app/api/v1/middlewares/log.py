from fastapi import status, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.utils.http import HttpClient
from app.response.error import ServerError
from app.logs import logging_




class LogMiddleware(BaseHTTPMiddleware):
     def __init__(self, *args, **kwargs) -> None:
          self.http_client = HttpClient()
          super().__init__(*args, **kwargs)
          
     
     async def dispatch(
          self, 
          request: Request, 
          call_next: RequestResponseEndpoint
     ):
          from_ = request.headers.get("FROM")
          if from_ is None:
               from_ = str(request.client)
               
          logging_.api.info(f"{from_} {request.method} {request.url}")
          
          try:
               return await call_next(request)
          except Exception as ex:
               logging_.api.error(exc_info=ex, msg="error")
               return await self.try_later(exec=ex)
               
               
     async def try_later(self, exec: str) -> JSONResponse:
          await self.http_client.send_exception_message(exec=exec)
          return ServerError.response()