from app.core.security import create_access_token
from app.core.dependencies import get_current_user

token = create_access_token(
    {
        "sub": "user_001",
        "role": "ADMIN"
    }
)

current_user = get_current_user(token)

print(current_user)