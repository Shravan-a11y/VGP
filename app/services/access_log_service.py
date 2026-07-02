from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException
from app.repositories.access_log_repository import (
    AccessLogRepository
)
from app.services.audit_log_service import (
    AuditLogService
)

from app.services.gate_pass_service import(
     GatePassService
)
class AccessLogService:

    def __init__(self):

        self.repository=AccessLogRepository()
        self.gate_pass_service=GatePassService()
        self.audit_service = AuditLogService()

    def record_entry(
    self,
    gatepass_id: str,
    ):
        validation = (
            self.gate_pass_service
            .validate_gate_pass(
                gatepass_id
            )
        )

        if not validation["valid"]:
            raise HTTPException(
            status_code=400,
            detail=validation["message"]
            )

        logs = self.repository.get_logs_by_gatepass(
            gatepass_id
        )

        for log in logs:
            if log["action"] == "ENTRY":
                raise HTTPException(
                status_code=400,
            detail="Visitor already entered"
            )

        log = {
            "log_id": str(uuid4()),
            "gatepass_id": gatepass_id,
            "action": "ENTRY",
            "timestamp": datetime.now().isoformat()
        }

        created_log = self.repository.create_log(
            log
)

        self.audit_service.log_action(
            action="ENTRY",
            user_id="SYSTEM",
            entity_id=gatepass_id
        )

        return created_log

    def record_exit(
            self,
            gatepass_id: str,
    ):
        validation = (
            self.gate_pass_service
            .validate_gate_pass(
                gatepass_id
            )
        )

        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail=validation["message"]
            )

        logs = self.repository.get_logs_by_gatepass(
            gatepass_id
        )

        entry_found = False

        for log in logs:
            if log["action"] == "ENTRY":
                entry_found = True

        if not entry_found:
            raise HTTPException(
                status_code=400,
                detail="Visitor has not entered yet"
            )

        for log in logs:
            if log["action"] == "EXIT":
                raise HTTPException(
                    status_code=400,
                    detail="Visitor already exited"
                )

        log = {
            "log_id": str(uuid4()),
            "gatepass_id": gatepass_id,
            "action": "EXIT",
            "timestamp": datetime.now().isoformat()
        }

        created_log = self.repository.create_log(
            log
        )

        self.gate_pass_service.deactivate_gate_pass(
            gatepass_id
        )

        self.audit_service.log_action(
            action="EXIT",
            user_id="SYSTEM",
            entity_id=gatepass_id
)

        return created_log