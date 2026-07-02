from fastapi import APIRouter,Depends
from app.services.access_log_service import (
    AccessLogService
)
from app.core.dependencies import(
    get_current_user,
    require_guard
)

router=APIRouter(
    prefix="/access_log",
    tags=["Access Log"]
)

service=AccessLogService()

@router.post("/entry/{gatepass_id}")

async def record_entry(
    gatepass_id:str,
    current_user=Depends(require_guard)
):

    return service.record_entry(
        gatepass_id
    )

@router.put("/exit/{gatepass_id}")

async def record_exit(
    gatepass_id:str,
    current_user=Depends(require_guard)
):
    return service.record_exit(
        gatepass_id
    )