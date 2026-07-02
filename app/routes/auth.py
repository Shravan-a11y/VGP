from fastapi import APIRouter, HTTPException,Depends
from app.services.auth_service import login_user
from app.core.dependencies import get_current_user,create_access_token

from app.models.auth import(
    LoginRequest,
    TokenResponse
)

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    login_data:LoginRequest
):
    token= login_user (
        login_data.email,
        login_data.password,
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )

@router.get("/profile")
async def profile(
    current_user=Depends(get_current_user)
):
    return current_user