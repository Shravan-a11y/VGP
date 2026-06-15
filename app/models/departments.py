from  datetime import datetime
from pydantic import BaseModel

class Department (BaseModel):
    department_id:str
    department_code:str
    department_name:str
    hod_id:str
    created_at:datetime