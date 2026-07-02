from fastapi import APIRouter,Depends

from app.services.audit_log_service import (
    AuditLogService
)
from app.core.dependencies import (
    require_admin
)
router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)

service = AuditLogService()

@router.get("/")
async def get_all_logs(
    current_user=Depends(require_admin)
):

    return service.get_all_logs()