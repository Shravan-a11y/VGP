from app.core.firebase import initialize_firebase

class AuditLogRepository:

    def __init__(self):
        self.db = initialize_firebase()

    def create_log(
            self,
            log_data: dict
    ):
        self.db.collection(
            "audit_logs"
        ).document(
            log_data["audit_id"]
        ).set(
            log_data
        )

        return log_data

    def get_all_logs(
        self
    ):
        docs = self.db.collection(
            "audit_logs"
            ).stream()

        logs = []

        for doc in docs:
            logs.append(
                doc.to_dict()
            )

        return logs


    def count_logs(
        self
    ):
        docs = self.db.collection(
            "audit_logs"
        ).stream()

        return len(
            list(docs)
        )