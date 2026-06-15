from datetime import date, datetime

from app.models.visitor_application import (
    VisitorApplication,
    ApplicationStatus,
)

application = VisitorApplication(
    application_id="app_001",
    visitor_name="John Smith",
    visitor_email="john@example.com",
    visitor_phone="9876543210",
    visitor_company="ABC Ltd",
    purpose="Project Discussion",
    host_employee_id="EMP001",
    department_id="dept_001",
    visit_date=date.today(),
    status=ApplicationStatus.PENDING,
    created_at=datetime.now(),
)

print(application)