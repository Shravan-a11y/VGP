from datetime import datetime
from pydantic import EmailStr,BaseModel

class User(BaseModel):
    user_id:str
    name:str
    email:EmailStr
    employee_id:str
    department_id:str
    role:str
    is_active:bool
    created_at:datetime
    