from typing import Callable, Awaitable
from datetime import datetime, timedelta
from fastapi import Request, Response

from starlette.middleware.base import (
     BaseHTTPMiddleware, 
     RequestResponseEndpoint
)
from app.response.error import RequestTimeout, HeadersError




class TimeoutMiddleware(BaseHTTPMiddleware):
     users = {
          "GET": {},
          "POST": {},
          "PATCH": {},
          "DELETE": {}
     }
     
     
     def __init__(
          self, 
          app,
          routes: dict[str, dict[str, timedelta]],
          main_path: str = "",
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
          user = request.headers.get("user")
          
          if user == "system":
               return await call_next(request)

          if not user:
               return HeadersError.response()
          
          for key, value in self.routes[method].items():
               if self.main_path:
                    key = self.main_path + key
               
               if key == path:
                    if key not in self.users[method]:
                         self.users[method].update({key: {}})
                         
                    if user not in self.users[method][key]:
                         self.users[method][key].update({user: datetime.utcnow() + value})
                         return await call_next(request)
                         
                    if datetime.utcnow() >= self.users[method][key][user]:
                         self.users[method][key][user] = datetime.utcnow() + value
                         return await call_next(request)
                    return RequestTimeout.response()