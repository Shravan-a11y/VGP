from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException
from app.repositories.gate_pass_repository import(
    GatePassRepository
)
from app.repositories.visitor_application_repository import(
    VisitorApplicationRepository
)

from app.core.qr_generator import generate_qrcode

class GatePassService :

    def __init__(self):
        self.gatepass_repository=GatePassRepository()
        self.application_repository=VisitorApplicationRepository()

    def generate_gate_pass(
            self,
            application_id:str
    ):
        application = (
            self.application_repository
            .get_application_by_id(application_id)
        )

        if not application:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        if application["status"]!="APPROVED":
            raise HTTPException(
                status_code=404,
                detail="Application not approved"
            )

        gate_pass = {
    "gatepass_id": str(uuid4()),
    "application_id": application_id,
    "visitor_name": application["visitor_name"],
    "visitor_email": application["visitor_email"],
    "visitor_phone": application["visitor_phone"],
    "purpose": application["purpose"],
    "visit_date": application["visit_date"],
    "expected_time": application["expected_time"],
    "host_id": application["host_id"],
    "status": "ACTIVE",
    "created_at": datetime.now().isoformat()
}

        qr_path=generate_qrcode(
            gate_pass["gatepass_id"]
        )
        gate_pass["qr_code_path"]=qr_path


        return self.gatepass_repository.create_gate_pass(
        gate_pass
    )

    def validate_gate_pass(
            self,
            gatepass_id:str
    ):
        gate_pass=(
            self.gatepass_repository
            .get_gate_pass_by_id(gatepass_id)

        )

        if not gate_pass:

            return{
                "valid":False,
                "message":"Gate Pass not found"
            }

        if  gate_pass["status"] !="ACTIVE":
            return{
                "valid":False,
                "message":"Gate Pass inactive"
            }

        return {
            "valid":True,
            "message":"Gate Pass valid",
            "gate_pass":gate_pass
        }


    def deactivate_gate_pass(
            self,
            gatepass_id: str
        ):
            return (
                self.gatepass_repository
                .update_gatepass_status(
                 gatepass_id,
                    "INACTIVE"
                )
            )