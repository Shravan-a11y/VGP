from app.core.security import (
    hash_password,
    verify_password
)

password="admin123"

hashed_password=hash_password(password)

print("Original Password:", password)
print("Hashed Password:",hashed_password)

is_valid=verify_password(
    password,
    hashed_password
)

print("Password Mach:",is_valid)