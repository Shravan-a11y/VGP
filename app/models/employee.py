from pydantic import BaseModel,EmailStr


class EmployeeCreate(BaseModel):

    employee_name:str
    employee_email:EmailStr
    department_id:str
    role:str
