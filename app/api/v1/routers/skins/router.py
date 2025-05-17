from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.response import is_response
from app.response.error import InvalidArguments
from app.schemas.v1 import SkinSchema
from .service import SkinService, get_skin_service
from .schema import SkinCreateArguments, SkinUpdateArguments



skins_router = APIRouter(
     prefix="/api/v1",
     tags=["Skin"]
)




@skins_router.get(
     path="/skin",
     summary="Get data about skin",
     responses={
          404: {
               "description": "Skin or user not exists",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SkinOrUserNotExists"
                         }
                    }
               }
          }
     }
)
async def get_skins(
     telegram_id: int,
     service: Annotated[SkinService, Depends(get_skin_service)],
     skin_id: int | None = None,
     skin_name: str | None = None
) -> SkinSchema:
     if any([skin_id, skin_name]) is False:
          return InvalidArguments.response()
     
     result = await service.get_skin(
          skin_id=skin_id,
          skin_name=skin_name,
          telegram_id=telegram_id
     )
     if await is_response(result) is True:
          return result.response()
     return result
     
     
     
     
@skins_router.post(
     path="/skin",
     summary="Skin created",
     responses={
          200: {
               "description": "SkinCreated",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SkinCreated"
                         }
                    }
               }
          },
          409: {
               "description": "SkinExists",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SkinExists"
                         }
                    }
               }
               
          },
          400: {
               "description": "Steam error",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "HttpError. Wait few minutes or check status Steam server"
                         }
                    }
               }
          },
          404: {
               "description": "User not exists",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "UserNotExists"
                         }
                    }
               }
          },
          1404: {
               "description": "Steam not found item",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SteamNotFoundItem"
                         }
                    }
               }
          }
     }
)
async def create_skin(
     telegram_id: int,
     arguments: SkinCreateArguments,
     service: Annotated[SkinService, Depends(get_skin_service)]
) -> JSONResponse:
     result = await service.create_skin(
          name=arguments.name,
          image=str(arguments.image),
          percent=arguments.percent,
          telegram_id=telegram_id
     )
     return result.response()
     
     
     
@skins_router.patch(
     path="/skin",
     responses={
          200: {
               "description": "Skin updated",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SkinUpdated"
                         }
                    }
               }
          },
          403: {
               "description": "Invalid arguments",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "InvalidArguments"
                         }
                    }
               }
          },
          404: {
               "description": "Skin or user not exists",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SkinOrUserNotExists"
                         }
                    }
               }
          }
          
     }
)
async def change_skin(
     service: Annotated[SkinService, Depends(get_skin_service)],
     arguments: SkinUpdateArguments,
     telegram_id: int,
     skin_id: int | None = None,
     skin_name: str | None = None
) -> JSONResponse:
     if any(arguments.values) is False or any([skin_id, skin_id]):
          return InvalidArguments.response()
     
     result = await service.change_skin(
          skin_id=skin_id,
          skin_name=skin_name,
          telegram_id=telegram_id,
          skin_data=arguments.non_nullable()
     )
     return result.response()
     
     
     
     
     
     
@skins_router.delete(
     path="/skin",
     responses={
          200: {
               "description": "Skin deleted",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SkinDeleted"
                         }
                    }
               }
          },
          403: {
               "description": "Invalid arguments",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "InvalidArguments"
                         }
                    }
               }
          },
          404: {
               "description": "Skin or user not exists",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "SkinOrUserNotExists"
                         }
                    }
               }
          }
     }
)
async def delete_skin(
     telegram_id: int,
     service: Annotated[SkinService, Depends(get_skin_service)],
     skin_id: int | None = None,
     skin_name: str | None = None
) -> JSONResponse:
     if any([skin_id, skin_name]) is False:
          return InvalidArguments.response()
     
     result = await service.delete_skin(
          telegram_id=telegram_id,
          skin_id=skin_id,
          skin_name=skin_name
     )
     return result.response()