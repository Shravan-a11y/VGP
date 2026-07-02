import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebase_app = None
firestore_db = None


def initialize_firebase():
    global firebase_app
    global firestore_db

    if firebase_app is None:
        cred = credentials.Certificate(
            "secrets/gatesystem-d022a-firebase-adminsdk-fbsvc-79960e5d37.json"
        )

        firebase_app = firebase_admin.initialize_app(
            cred
        )

        firestore_db = firestore.client()

    return firestore_db