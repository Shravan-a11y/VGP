from app.repositories.department_repository import(
    DepartmentRepository
)

repo=DepartmentRepository()


department={
    "deparment_name":"IT",
    "host_id":"INT_190"
}

result=repo.create_department(
    department
)

print (result)
