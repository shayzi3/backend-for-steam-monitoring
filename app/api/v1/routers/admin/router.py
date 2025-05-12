from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, FileResponse

from .service import AdminService, get_admin_service



admin_router = APIRouter(
     prefix="/api/v1",
     tags=["Admin"]
)

     
     
@admin_router.get("/admin/logs")
async def download_logs(
     service: Annotated[AdminService, Depends(get_admin_service)]
) -> FileResponse:
     ...
     
     

     
