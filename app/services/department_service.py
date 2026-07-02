from uuid import uuid4
from datetime import datetime
from app.repositories.department_repository import(
    DepartmentRepository
)

from app.models.department import(
    DepartmentCreate
)




class DeparmentService:

    def __init__(self):
        self.repository=DepartmentRepository()

    def create_department(
            self,
            department_data:dict
    ):
        department = {
            "department_id": str(uuid4()),
            "department_code": department_data.department_code,
            "department_name": department_data.department_name,
            "hod_id": department_data.hod_id,
            "created_at": datetime.now().isoformat()
        }

        return self.repository.create_department(
            department
        )

    def get_department_by_id(
            self,
            department_id:str
    ):
        return self.repository.get_department_by_id(
            department_id
        )

    def get_all_departments(
            self,

    ):
        return self.repository.get_all_departments()

    def assign_hod(
        self,
        department_id: str,
        employee_id: str
    ):
        return (
            self.repository
            .assign_hod(
                department_id,
                employee_id
            )
        )