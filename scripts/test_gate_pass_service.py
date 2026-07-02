from app.services.gate_pass_service import (
    GatePassService
)

service = GatePassService()

result = service.generate_gate_pass(
    "207d410b-7a3a-431d-9da6-b4674e192ba9"
)

print(result)