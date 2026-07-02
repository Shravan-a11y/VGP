from app.repositories.visitor_application_repository import (
    VisitorApplicationRepository
)

repo = VisitorApplicationRepository()

result = repo.update_application_status(
    "20984abd-664c-4b6b-bb01-5670c53b5e6a",
    "APPROVED"
)

print(result)