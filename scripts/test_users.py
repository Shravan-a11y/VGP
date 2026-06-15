from datetime import datetime
from app.models.users import User



user = User(
    user_id="user_001",
    name="Shravan Deshmukh",
    email="shravan@example.com",
    employee_id="EMP001",
    department_id="dept_001",
    role="ADMIN",
    is_active=True,
    created_at=datetime.now()
)

print(user)
