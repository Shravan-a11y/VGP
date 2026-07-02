from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from app.repositories.visitor_application_repository import (
    VisitorApplicationRepository
)
from app.models.visitor_application import VisitorApplicationCreate

from app.services.gate_pass_service import(
    GatePassService
)

from app.repositories.employee_repository import(
    EmployeeRepository
)

from app.services.audit_log_service import (
    AuditLogService
)

class VisitorApplicationService:
    def __init__(self):
        self.repository=VisitorApplicationRepository()
        self.gate_pass_service=GatePassService()
        self.employee_repository=EmployeeRepository()
        self.audit_service = AuditLogService()

    


    def submit_application(
    self,
    application_data: VisitorApplicationCreate,
    current_user: dict
    ):
        hod=(
            self.employee_repository
            .get_hod_by_department(
                application_data.department_id
            )
        )

        if not hod :
            raise ValueError(
                "No HOD found for the department "
            )

        application = {
    "application_id": str(uuid4()),

    "visitor_name": application_data.visitor_name,
    "visitor_email": application_data.visitor_email,
    "visitor_phone": application_data.visitor_phone,

    "purpose": application_data.purpose,

    "department_id": application_data.department_id,

    "visit_date": str(application_data.visit_date),
    "expected_time": application_data.expected_time,

    "host_id": hod["employee_id"],

    "status": "PENDING",

    "created_by": current_user["user_id"],

    "created_at": datetime.now().isoformat()
}

        created_application = (
            self.repository.create_application(
                application
        )
        )

        self.audit_service.log_action(
            action="CREATE_VISITOR_APPLICATION",
            user_id=current_user["user_id"],
            entity_id=application["application_id"]
)

        return created_application



    def get_application_by_id(
    self,
    application_id: str
    ):
        return self.repository.get_application_by_id(
        application_id
    )

    def get_all_applications(self):

        return self.repository.get_all_applications()




    def approve_application(
            self,
            application_id:str,
            current_user:dict
    ):
        application=self.repository.get_application_by_id(
            application_id
        )

        if not application:
            raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

        if application["host_id"] != current_user["employee_id"]:
            raise HTTPException(
            status_code=403,
            detail="You are not authorized to approve this application"
        )


        
        self.repository.update_application_status(
            application_id,
            "APPROVED"
        )

        self.audit_service.log_action(
            action="APPROVE_APPLICATION",
        user_id=current_user["user_id"],
        entity_id=application_id
        )

        gate_pass=self.gate_pass_service.generate_gate_pass(
            application_id
        )
        return {
            "message":"Application approved",
            "gate_pass":gate_pass
        }



    

    def reject_application(
            self,
            application_id:str,
            current_user:dict
    ):

        application=self.repository.get_application_by_id(
                    application_id
                )
        
        if not application:
            raise HTTPException(
            status_code=404,
            detail="Application not found"
                )
        
        if application["host_id"] != current_user["employee_id"]:
            raise HTTPException(
            status_code=403,
            detail="You are not authorized to approve this application"
                )
        
        self.repository.update_application_status(
            application_id,
            "REJECTED"
        )

        self.audit_service.log_action(
            action="REJECT_APPLICATION",
            user_id=current_user["user_id"],
            entity_id=application_id
        )

        return {
            "application_id": application_id,
            "status": "REJECTED"
        }


    def get_pending_applications_for_hod(
           self,
           hod_id: str
       ):
   
           return (
               self.repository
               .get_pending_applications_by_hod(
                   hod_id
               )
           )