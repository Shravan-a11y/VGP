from app.core.dependencies import require_admin

current_user={
    "user_id":"user_001",
    "role":"ADMIN"
}

result=require_admin(current_user)

print(result)