from uuid import uuid4
from datetime import datetime

from app.repositories.audit_log_repository import (
    AuditLogRepository
)

class AuditLogService:

    def __init__(self):
        self.repository = AuditLogRepository()

    def log_action(
            self,
            action: str,
            user_id: str,
            entity_id: str
    ):
        log = {
            "audit_id": str(uuid4()),
            "action": action,
            "user_id": user_id,
            "entity_id": entity_id,
            "timestamp": datetime.now().isoformat()
        }

        return self.repository.create_log(
            log
        )

    def get_all_logs(
        self
    ):
        return self.repository.get_all_logs()