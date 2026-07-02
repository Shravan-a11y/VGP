from app.repositories.visitor_application_repository import (
    VisitorApplicationRepository
)
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.gate_pass_repository import GatePassRepository
from app.repositories.audit_log_repository import AuditLogRepository

class DashboardService:

    def __init__(self):
        self.application_repository = (
            VisitorApplicationRepository()
        )

        self.employee_repository = EmployeeRepository()
        self.department_repository = DepartmentRepository()
        self.gatepass_repository = GatePassRepository()
        self.audit_repository = AuditLogRepository()

    def get_hod_dashboard(
            self,
            hod_id: str
    ):
        applications = (
            self.application_repository
            .get_applications_by_hod(
                hod_id
            )
        )

        pending = 0
        approved = 0
        rejected = 0

        for application in applications:

            if application["status"] == "PENDING":
                pending += 1

            elif application["status"] == "APPROVED":
                approved += 1

            elif application["status"] == "REJECTED":
                rejected += 1

        return {
            "pending_applications": pending,
            "approved_applications": approved,
            "rejected_applications": rejected,
            "total_applications": len(
                applications
            )
        }

    def get_admin_dashboard(self):

        return {
        "total_visitors":
            self.application_repository
            .count_applications(),

        "total_employees":
            self.employee_repository
            .count_employees(),

        "total_departments":
            self.department_repository
            .count_departments(),

        "active_gatepasses":
            self.gatepass_repository
            .count_active_gatepasses()
        }

    def get_admin_dashboard(
        self
    ):
        return {
            "total_visitors":
                self.application_repository
                .count_applications(),

            "total_employees":
                self.employee_repository
                .count_employees(),

            "total_departments":
                self.department_repository
                .count_departments(),

            "active_gatepasses":
                self.gatepass_repository
                .count_active_gatepasses(),

            "audit_logs":
                self.audit_repository
                .count_logs()
        }