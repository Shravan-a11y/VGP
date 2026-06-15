from datetime import datetime
from pydantic import BaseModel


class AuditLog(BaseModel):

    audit_id:str
    user_id: str
    action: str
    resource: str
    timestamp: datetime