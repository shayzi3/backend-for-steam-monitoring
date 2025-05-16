from fastapi import FastAPI

from .user.router import user_router
from .skins.router import skins_router


__routers__ = [
     user_router,
     skins_router,
]


def include_routers(app: FastAPI) -> None:
     for router in __routers__:
          app.include_router(router)