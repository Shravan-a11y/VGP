from datetime import datetime

from app.models.audit_log import AuditLog


audit = AuditLog(
    audit_id="audit_001",
    user_id="user_001",
    action="APPROVE_APPLICATION",
    resource="app_001",
    timestamp=datetime.now(),
)

print(audit)