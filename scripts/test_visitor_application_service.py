from app.services.visitor_application_service import (
    VisitorApplicationService
)

service = VisitorApplicationService()

application = service.submit_application(
    {
        "visitor_name": "Rahul Sharma",
        "visitor_phone": "9876543210",
        "purpose": "Project Discussion",
        "host_id": "user_001"
    },
    {
        "user_id": "user_001",
        "role": "ADMIN"
    }
)

print(application)