from fastapi import Request

from app.response.error import InvalidToken
from app.core.security import verify_token
from app.logs import logging_


async def validate_unique_token(request: Request) -> None:
    token = request.headers.get("API")
    service = request.headers.get("FROM")
    
    if (token is None) or (service is None) or (service not in ["BOT", "WEB"]):
        logging_.http.error(f"TOKEN NOT VALID: {token}")
        return InvalidToken.response()
        
    access = await verify_token(token=token, service=service)
    if access is False:
        logging_.http.error(f"TOKEN NOT VALID: {token}")
        return InvalidToken.response()
    
        
    
        
    