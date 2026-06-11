import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from app.core.config import settings

firebase_app=None

def initialize_firebase():
    global firebase_app

    if firebase_app is None:
        cred =credentials.Certificate(
            "secrets/gate-pass-system-9a932-firebase-adminsdk-fbsvc-4475b46c50.json"
        )
        firebase_app=firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": settings.FIREBASE_DATABASE_URL
            }
        )

    return firebase_app