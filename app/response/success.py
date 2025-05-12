from fastapi import status

from .abstract_response import BaseJsonResponse


     

class UserCreated(BaseJsonResponse):
     content = "UserCreated"
     status_code = status.HTTP_200_OK
     
     
     
class UserUpdated(BaseJsonResponse):
     content = "UserUpdated"
     status_code = status.HTTP_200_OK
     
     
     
class SkinCreated(BaseJsonResponse):
     content = "SkinCreated"
     status_code = status.HTTP_200_OK
     
     
     
class SkinUpdated(BaseJsonResponse):
     content = "SkinUpdated"
     status_code = status.HTTP_200_OK
     
     
     
class SkinDeleted(BaseJsonResponse):
     content = "UserDeleted"
     status_code = status.HTTP_200_OK
     
     




          
          
