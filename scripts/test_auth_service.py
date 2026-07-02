from app.services.auth_service import login_user

token =login_user(
    "admin@example.com",
    "admin123"
)

print(token)
