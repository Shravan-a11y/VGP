from pydantic import BaseModel

class AccessLog(BaseModel):
    log_id:str
    gatepass_id:str
    action:str
    timestamp:str