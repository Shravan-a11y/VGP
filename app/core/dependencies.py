from app.core.config import settings
from app.core.security import verify_token,create_access_token
from app.core.roles import UserRole
from fastapi.security import OAuth2PasswordBearer,HTTPBearer
from fastapi import Depends
from fastapi import HTTPException
from app.core.roles import UserRole

security=HTTPBearer()
oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_settings():
    return settings

from fastapi.security import HTTPAuthorizationCredentials

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    return {
        "user_id": payload["sub"],
        "employee_id":payload["employee_id"],
        "role": payload["role"]
    }

def require_hod(
        current_user=Depends(get_current_user)
):
    if current_user["role"]!=UserRole.HOD:
        raise HTTPException(
            status_code=403,
            detail="HOD access Required"
        )

    return current_user


def require_admin(
    current_user=Depends(get_current_user)
):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user

def require_guard(
    current_user=Depends(get_current_user)
):
    if current_user["role"] != UserRole.GUARD:
        raise HTTPException(
            status_code=403,
            detail="Security access Required"
        )

    return current_user