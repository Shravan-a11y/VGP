from fastapi import Request, HTTPException


def get_session_user(request: Request):

    user = request.session.get("user")

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )

    return user


def require_admin(request: Request):

    user = get_session_user(request)

    if user["role"] != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user


def require_hod(request: Request):

    user = get_session_user(request)

    if user["role"] != "HOD":
        raise HTTPException(
            status_code=403,
            detail="HOD access required"
        )

    return user


def require_guard(request: Request):

    user = get_session_user(request)

    if user["role"] != "GUARD":
        raise HTTPException(
            status_code=403,
            detail="Guard access required"
        )

    return user