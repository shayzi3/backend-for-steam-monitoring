import uvicorn
import asyncio

from datetime import timedelta
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.routers import include_routers
from app.api.v1.dependency.user import validate_unique_token
from app.api.v1.middlewares import LogMiddleware, TimeoutMiddleware
from app.workers.monitoring import MonitoringWorker
from app.db.sql.repository import UserRepository, SkinRepository
from app.utils.http import HttpClient



@asynccontextmanager
async def lifespan(_: FastAPI):
     monitoring = MonitoringWorker(
          user_repository=UserRepository,
          skin_repository=SkinRepository,
          http_client=HttpClient()
     )
     asyncio.create_task(monitoring.run())
     yield


app = FastAPI(
          title="SteamMotorBackend",
          responses={
               401: {
                    "description": "Invalid token",
                    "content": {
                         "application/json": {
                              "example": {
                                   "detail": "InvalidToken"
                              }
                         }
                    }
               },
               408: {
                    "description": "Request timeout",
                    "content": {
                         "apllication/json": {
                              "example": {
                                   "detail": "RequestTimeout"
                              }
                         }
                    }
               },
               500: {
                    "description": "Server Error",
                    "content": {
                         "application/json": {
                              "example": {
                                   "detail": "TryLater"
                              }
                         }
                    }
               },
               405: {
                    "description": "In headers must be telegram id. Field 'user'",
                    "content": {
                         "application/json": {
                              "example": {
                                   "detail": "NotFoundInHadersTelegramID"
                              }
                         }
                    }
               }
          },
          dependencies=[Depends(validate_unique_token)],
          lifespan=lifespan
     )
app.add_middleware(
     TimeoutMiddleware, 
     main_path="/api/v1",
     routes={
          "GET": {
               "/user": timedelta(seconds=1),
               "/skin": timedelta(seconds=1)
          },
          "POST": {
               "/user": timedelta(seconds=2),
               "/skin": timedelta(seconds=2)
          },
          "PATCH": {
               "/user": timedelta(seconds=4),
               "/skin": timedelta(seconds=4)
          },
          "DELETE": {
               "/skin": timedelta(seconds=1)
          }
     }
)
app.add_middleware(LogMiddleware)
app.add_middleware(
     CORSMiddleware,
     allow_origins=[
          "http://localhost",
          "http://localhost:8083"
     ],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"]
)
include_routers(app)





if __name__ == "__main__":
     uvicorn.run(
          "main:app", 
          port=8084, 
          host="localhost",
          reload=True
     )