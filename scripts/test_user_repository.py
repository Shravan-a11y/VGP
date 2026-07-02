from app.repositories.user_repository import UserRepository

repo = UserRepository()

user = repo.get_user_by_email(
    "admin@example.com"
)

print(user)