from uuid import uuid4
from datetime import datetime 
from app.core.security import hash_password
from fastapi import HTTPException
from app.models.employee import(
    EmployeeCreate
)


from app.repositories.employee_repository import(
    EmployeeRepository
)

from app.repositories.department_repository import(
    DepartmentRepository
)

from app.repositories.user_repository import(
    UserRepository
)

from app.services.access_log_service import(
     AuditLogService
)
class EmployeeService:


    def __init__(self):
        self.repository=EmployeeRepository()
        self.department_repository=DepartmentRepository()
        self.user_repository=UserRepository()
        self.audit_service=AuditLogService()


    def create_employee(
            self,
            employee_data:EmployeeCreate
    ):

        depatment=(
            self.department_repository
            .get_department_by_id(
                employee_data.department_id
            )
        )

        if not depatment:
            raise HTTPException(
                status_code=404,
                detail="Department Not Found"
            )

        
        if (
            employee_data.role == "HOD"
            and depatment.get("hod_id")
        ):
            raise HTTPException(
                status_code=400,
                detail="This department already has a HOD assigned."
            )

        employee = {
            "employee_id": str(uuid4()),
            "employee_name": employee_data.employee_name,
            "employee_email": str(
                employee_data.employee_email
            ),
            "department_id": employee_data.department_id,
            "role": employee_data.role,
            "created_at": datetime.now().isoformat()
        }

        created_employee=self.repository.create_employee(
            employee
        )

        self.audit_service.log_action(
            action="CREATE_EMPLOYEE",
            user_id="SYSTEM",
            entity_id=employee["employee_id"]
        )

        # Automatically assign HOD to the department
        if employee["role"] == "HOD":

            self.department_repository.assign_hod(
                employee["department_id"],
                employee["employee_id"]
            )



        if employee["role"] in[
                "HOD",
                "ADMIN",
                "GUARD"
            ]:
            

                user = {
                "user_id": str(uuid4()),
                "employee_id": employee["employee_id"],
                "name": employee["employee_name"],
                "email": employee["employee_email"],
                "hashed_password": hash_password(
                "ChangeMe123"
                ),
                "role": employee["role"],
                "department_id": employee["department_id"],
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }

                self.user_repository.create_user(
                    user
                )

        
        return created_employee

    def get_employee_by_id(
            self,
            employee_id:str
    ):

        return self.repository.get_employee_by_id(
            employee_id
        )


    def get_all_employees(
            self
    ):

        return self.repository.get_all_employees()


    def update_employee(
    self,
    employee_id: str,
    employee_name: str,
    employee_email: str,
    department_id: str,
    role: str
    ):

        employee = self.repository.get_employee_by_id(
            employee_id
        )

        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        updated_employee = {

            "employee_name": employee_name,

            "employee_email": employee_email,

            "department_id": department_id,

            "role": role

        }

        self.repository.update_employee(
            employee_id,
            updated_employee
        )

        return updated_employee