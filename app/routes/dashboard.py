from fastapi import APIRouter, Depends

from app.core.dependencies import (
    require_hod
)
from app.core.dependencies import(
    get_current_user,
    require_admin
)

from app.services.dashboard_service import (
    DashboardService
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

service = DashboardService()

@router.get("/hod")
async def hod_dashboard(
    current_user=Depends(
        require_hod
    )
):
    return service.get_hod_dashboard(
        current_user["employee_id"]
    )

@router.get("/admin")
async def admin_dashboard(
    current_user=Depends(
        require_admin
    )
):
    return service.get_admin_dashboard()

