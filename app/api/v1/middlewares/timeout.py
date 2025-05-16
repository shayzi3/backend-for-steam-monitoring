from typing import Callable, Awaitable
from datetime import datetime, timedelta
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp




class TimeoutMiddleware(BaseHTTPMiddleware):
     users = {}
     
     
     def __init__(
          self, 
          app: ASGIApp,
          routes: dict[str, dict[str, timedelta]],
          main_path: str = ""
     ) -> None:
          self.routes = routes
          self.main_path = main_path
          super().__init__(app)
          
          
     async def dispatch(
          self, 
          request: Request, 
          call_next: RequestResponseEndpoint
     ) -> Callable[[Request], Awaitable[Response]]:
          method = request.method
          path = request.url.components.path
          client = str(request.client.host) + ":" + str(request.client.port)
          
          for key, value in self.routes[method].items():
               if self.main_path:
                    key = self.main_path + key
               
               if key == path:
                    if client not in self.users:
                         self.users[client] = datetime.utcnow() + value
                         
                    if datetime.utcnow() <= self.users[client]:
                         self.users[client] = datetime.utcnow() + value
                         return await call_next(request)
                    return await self.try_later()
          
     async def try_later(self) -> JSONResponse:
          return JSONResponse(
               content={"detail": "RequestTImeout"},
               status_code=status.HTTP_408_REQUEST_TIMEOUT
          )