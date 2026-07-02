from app.repositories.user_repository import UserRepository
from app.core.security import(
    hash_password,
    verify_password,
    create_access_token
)

user_repository=UserRepository()

def authenticate_user(
        email:str,
        password:str
):
    user=user_repository.get_user_by_email(
        email
    )

    if not user:
        return None

    if not verify_password(
        password,
        user["hashed_password"]
    ):
        return None

    return user


def login_user(
    email: str,
    password: str
):

    user = authenticate_user(
        email,
        password
    )

    if not user:
        return None

    token = create_access_token(
        {
            "sub": user["user_id"],
            "employee_id":user["employee_id"],
            "role": user["role"]
        }
    )

    return token