from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DepartmentCreate(BaseModel):
    department_name:str
    hod_id:Optional[str]=None
    department_code:str

