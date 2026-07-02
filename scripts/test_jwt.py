from app.core.security import create_access_token

token = create_access_token(
    {
        "sub": "user_001",
        "role": "ADMIN"
    }
)

print("JWT Token:")
print(token)