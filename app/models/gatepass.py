from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class GatePassStatus(str,Enum):
    ACTIVE="ACTIVE"
    EXPIRED="EXPIRED"
    USED="USED"
    CANCELLED="CANCELLED"

class GatePass(BaseModel):

    pass_id: str
    application_id: str
    qr_code: str
    valid_from: datetime
    valid_until: datetime
    status: GatePassStatus
    generated_by: str
    generated_at: datetime

