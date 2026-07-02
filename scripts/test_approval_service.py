from app.services.visitor_application_service import (
    VisitorApplicationService
)

service = VisitorApplicationService()

result = service.reject_application(
    "20984abd-664c-4b6b-bb01-5670c53b5e6a"
)

print(result)