from datetime import datetime
from app.core.firebase import initialize_firebase
from app.core.security import hash_password


db = initialize_firebase()


admin_user={
    "user_id":"user_001",
    "name":"Shravan",
    "email":"admin@example.com",
    "employee_id":"EMP001",
    "department_id":"dept_001",
    "role":"ADMIN",
    "is_active":True,
    "hashed_password":hash_password("admin123"),
    "created_at":datetime.now().isoformat()
}

db.collection("users").document(
    admin_user["user_id"]

).set(admin_user)

print("Admin user created succesfully")