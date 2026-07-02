from app.repositories.employee_repository import (
    EmployeeRepository
)

repo = EmployeeRepository()

hod = repo.get_hod_by_department(
    "68cd0e92-6ca8-42ea-82fd-e0132bc6e560"
)

print(hod)