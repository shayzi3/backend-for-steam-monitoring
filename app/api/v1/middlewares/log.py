from fastapi import status, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.logs import logging_




class LogMiddleware(BaseHTTPMiddleware):
     
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
               return await self.try_later()
               
               
     async def try_later(self) -> JSONResponse:
          # оповощение ошибки, отправка в бота
          return JSONResponse(
               content={"detail": "TryLater"},
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
          )