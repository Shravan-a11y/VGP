from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AccessLog(BaseModel):

    log_id:str
    log_id: str
    pass_id: str
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None
    guard_id: str