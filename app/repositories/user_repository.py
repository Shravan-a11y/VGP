from google.cloud import firestore
from app.core.firebase import initialize_firebase


class UserRepository:

    def __init__(self):
        self.db=initialize_firebase()

    def get_user_by_email(self,email:str):

        users_ref=self.db.collection("users")

        query=users_ref.where(
            "email",
            "==",
            email
        ).limit(1)

        docs=query.stream()

        for doc in docs:
            return doc.to_dict()

        return None

    def create_user(self,user_data:dict):

        self.db.collection("users").document(
            user_data["user_id"]

        ).set(user_data)

        return user_data

