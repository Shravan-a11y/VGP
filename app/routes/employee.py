from fastapi import APIRouter,Depends
from app.services.employee_service import(
    EmployeeService
)

from app.models.employee import(
    EmployeeCreate
)

from app.core.dependencies import (
    get_current_user,
    require_admin
)


router=APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

service=EmployeeService()

@router.post("/")
async def create_employee(
    employee_data:EmployeeCreate,
    current_user=Depends(require_admin)
):
    return service.create_employee(
        employee_data
    )


@router.get("/")
async def get_all_employees(
    current_user=Depends(get_current_user)
):
    return service.get_all_employees()


@router.get("/{employee_id}")
async def get_employee_by_id(
    employee_id:str,
    current_user=Depends(get_current_user)
):

    return service.get_employee_by_id(
        employee_id
    )