import uvicorn

from fastapi import FastAPI, Depends

from app.api.v1.routers import include_routers
from app.api.v1.dependency.user import validate_unique_token



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
               }
          },
          dependencies=[Depends(validate_unique_token)]
     )
include_routers(app)


     

if __name__ == "__main__":
     uvicorn.run(
          "main:app", 
          port=9091, 
          reload=True, 
          host="localhost"
     )