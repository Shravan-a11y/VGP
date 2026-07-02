from app.repositories.gate_pass_repository import (
    GatePassRepository
)

repo = GatePassRepository()

gate_pass = {
    "gatepass_id": "GP001",
    "application_id": "APP001",
    "visitor_name": "Rahul Sharma",
    "host_id": "user_001",
    "status": "ACTIVE",
    "created_at": "2026-06-16"
}

result = repo.create_gate_pass(
    gate_pass
)

print(result)