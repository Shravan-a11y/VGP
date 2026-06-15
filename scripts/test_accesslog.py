from datetime import datetime

from app.models.accessLog import AccessLog


log = AccessLog(
    log_id="log_001",
    pass_id="pass_001",
    entry_time=datetime.now(),
    guard_id="user_003"
)

print(log)