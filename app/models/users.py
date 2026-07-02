from datetime import datetime
from pydantic import EmailStr,BaseModel
from app.core.roles import UserRole

class User(BaseModel):
    user_id:str
    name:str
    email:EmailStr
    employee_id:str
    department_id:str
    role:UserRole
    is_active:bool
    created_at:datetime
    