from app.models.auth import LoginRequest

login = LoginRequest(
    email="admin@example.com",
    password="admin123"
)

print(login)