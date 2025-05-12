from fastapi import status

from .abstract_response import BaseJsonResponse



class InvalidToken(BaseJsonResponse):
     content = "InvalidToken"
     status_code = status.HTTP_401_UNAUTHORIZED
     
     

class InvalidArguments(BaseJsonResponse):
     content = "InvalidArguments"
     status_code = status.HTTP_403_FORBIDDEN
     
     

class UserExists(BaseJsonResponse):
     content = "UserExists"
     status_code = status.HTTP_409_CONFLICT
     
     
     
class UserNotExists(BaseJsonResponse):
     content = "UserNotExists"
     status_code = status.HTTP_404_NOT_FOUND
     
     
     
class SkinExists(BaseJsonResponse):
     content = "SkinExists"
     status_code = status.HTTP_409_CONFLICT
     
     
     
class SkinNotExists(BaseJsonResponse):
     content = "SkinNotExists"
     status_code = status.HTTP_404_NOT_FOUND
     
     
     
class HttpStatusCodeError(BaseJsonResponse):
     content = "HttpStatusCodeError. Try request after few minutes"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
     
class HttpError(BaseJsonResponse):
     content = "HttpError. Try request after few minutes"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
     
class SteamNotFoundItem(BaseJsonResponse):
     content = "SteamNotFoundItem"
     status_code = 1404