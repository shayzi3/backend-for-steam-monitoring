from typing import Annotated
from datetime import timedelta
from fastapi import (
     APIRouter, 
     Depends,
     BackgroundTasks,
)
from fastapi.responses import JSONResponse

from app.response.success import UserUpdated
from app.response import is_response
from app.response.error import InvalidArguments
from app.schemas.v1 import UserSchema
from .service import get_user_service, UserService
from .schema import UserUpdateArguments, UserCreateArguments



user_router = APIRouter(
     prefix="/api/v1",
     tags=["User"],
)



@user_router.post(
     path="/user",
     summary="Create new user",
     responses={
          409: {
               "description": "User already exists",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "UserExists"
                         }
                    }
               }
          },
          200: {
               "description": "User success created",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "UserCreated"
                         }
                    }
               }
          }
     }
)
async def create_user(
     arguments: UserCreateArguments,
     service: Annotated[UserService, Depends(get_user_service)]
) -> JSONResponse:
     create_status = await service.create_user(
          telegram_id=arguments.telegram_id,
          telegram_username=arguments.telegram_username,
          language=arguments.language.value,
          currency=arguments.currency.int_value
     )
     return create_status.response()




@user_router.get(
     path="/user",
     summary="Get user by telegram_id or unique_id",
     responses={
          404: {
               "description": "User not exists",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "UserNotExists"
                         }
                    }
               }
          }
     }
)
async def get_user(
     service: Annotated[UserService, Depends(get_user_service)],
     telegram_id: int
) -> UserSchema:
     result = await service.get_user(telegram_id=telegram_id)
     if await is_response(result) is True:
          return result.response()
     return result




@user_router.patch(
     path="/user",
     summary="Update data at user",
     responses={
          200: {
               "description": "User success updated",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "UserUpdated"
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
          403: {
               "description": "Invalid arguments",
               "content": {
                    "application/json": {
                         "example": {
                              "detail": "InvalidArguments"
                         }
                    }
               }
          }
     }
)
async def update_user(
     telegram_id: int,
     service: Annotated[UserService, Depends(get_user_service)],
     arguments: UserUpdateArguments,
     background_task: BackgroundTasks
) -> JSONResponse:
     if any(arguments.values) is False:
          return InvalidArguments.response()
     
     result = await service.update_user(
          telegram_id=telegram_id,
          not_nullable_value=arguments.non_nullable()
     )
     if result is UserUpdated:
          if "currency" in arguments.non_nullable():
               background_task.add_task(
                    service.change_price_of_skins,
                    telegram_id=telegram_id
               )
               
          if "timer" in arguments.non_nullable():
               background_task.add_task(
                    service.set_time_in_redis,
                    periodic_time=arguments.timer,
                    telegram_id=telegram_id
               )
     return result.response()
     