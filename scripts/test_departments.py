from app.models.departments import Department
from datetime import datetime

department = Department(
    department_id="dept_001",
    department_name="Information Technology",
    hod_id="user_001",
    created_at=datetime.now()
)

print(department)