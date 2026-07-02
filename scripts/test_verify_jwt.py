from app.core.security import (
    create_access_token,
    verify_token
)

token = create_access_token(
    {
        "sub": "user_001",
        "role": "ADMIN"
    }
)

print("Token:")
print(token)

payload = verify_token(token)

print("\nDecoded Payload:")
print(payload)