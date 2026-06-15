from datetime import datetime ,timedelta

from app.models.gatepass import(
    GatePass,
    GatePassStatus,
)

gate_pass = GatePass(
    pass_id="pass_001",
    application_id="app_001",
    qr_code="GP-2026-001",
    valid_from=datetime.now(),
    valid_until=datetime.now() + timedelta(hours=8),
    status=GatePassStatus.ACTIVE,
    generated_by="user_001",
    generated_at=datetime.now(),
)

print(gate_pass)