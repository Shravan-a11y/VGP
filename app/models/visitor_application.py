from datetime import datetime,date
from enum import Enum
from pydantic import BaseModel,EmailStr,Field,field_validator

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

class VisitorApplicationCreate(BaseModel):

    visitor_name: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    visitor_email: EmailStr

    visitor_phone: str = Field(
        ...,
        min_length=10,
        max_length=10
    )

    purpose: str = Field(
        ...,
        min_length=5,
        max_length=150
    )

    visit_date: date

    expected_time: str

    department_id: str

    @field_validator("visitor_name")
    @classmethod
    def validate_name(cls, value):

        value = value.strip()

        if not value.replace(" ", "").isalpha():
            raise ValueError(
                "Visitor name should contain only letters and spaces."
            )

        return value

    @field_validator("visitor_phone")
    @classmethod
    def validate_phone(cls, value):

        if not value.isdigit():
            raise ValueError(
                "Phone number should contain only digits."
            )

        if len(value) != 10:
            raise ValueError(
                "Phone number must be exactly 10 digits."
            )

        return value

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, value):

        return value.strip()