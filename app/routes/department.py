from fastapi import APIRouter,Depends

from app.services.department_service import(
    DeparmentService
)

from app.models.department import(
    DepartmentCreate
)
from app.core.dependencies import(
    get_current_user,
    require_admin
)
router=APIRouter (
    prefix="/departments",
    tags=["Departments"]
)

service=DeparmentService()

@router.post("/")
async def create_department(
    department_data:DepartmentCreate,
    current_user=Depends(require_admin)
):
    return service.create_department(
        department_data
    )

@router.get("/")
async def get_all_department(
    current_user=Depends(get_current_user)
):

    return service.get_all_departments()

@router.get("/{department_id}")
async def get_department_by_id(
    department_id:str,
    current_user=Depends(get_current_user)
):

    return service.get_department_by_id(
        department_id
    )

@router.put("/{department_id}/assign-hod")
async def assign_hod(
    department_id: str,
    employee_id: str,
    current_user=Depends(require_admin)
):
    return service.assign_hod(
        department_id,
        employee_id
    )