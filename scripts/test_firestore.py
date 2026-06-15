from app.core.firebase import initialize_firebase

db = initialize_firebase()

db.collection("test").document("connection").set(
    {
        "status": "working"
    }
)

print("Firestore Write Successful")