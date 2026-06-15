from datetime import datetime,date
from enum import Enum
from pydantic import BaseModel,EmailStr

class ApplicationStatus(str,Enum):
    PENDING="PENDING"
    APPROVED="APPROVED"
    REJECTED="REJECTED"

class VisitorApplication(BaseModel):
    application_id: str

    visitor_name: str
    visitor_email: EmailStr
    visitor_phone: str
    visitor_company: str
    purpose: str
    host_employee_id: str
    department_id: str
    visit_date: date
    status: ApplicationStatus
    created_at: datetime