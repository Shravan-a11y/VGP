from pydantic import BaseModel

class GatePass(BaseModel):
    gatepass_id: str
    application_id: str
    visitor_name: str
    host_id: str
    status: str
    created_at: str