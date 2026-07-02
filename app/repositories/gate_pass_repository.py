from app.core.firebase import initialize_firebase

class GatePassRepository:

    def __init__(self):
        self.db=initialize_firebase()

    def create_gate_pass(
            self,
            gate_pass_data:dict
    ):
        self.db.collection(
            "gate_passes"
        ).document(
            gate_pass_data["gatepass_id"]
        ).set(
            gate_pass_data
        )

        return gate_pass_data

    def get_gate_pass_by_id(
    self,
    gatepass_id: str
    ):

        doc = self.db.collection(
        "gate_passes"
            ).document(
                gatepass_id
            ).get()

        if doc.exists:
            return doc.to_dict()

        return None

    def get_gate_pass_by_application_id(
    self,
    application_id: str
    ):

        docs = self.db.collection(
            "gate_passes"
        ).stream()

        for doc in docs:

            gatepass = doc.to_dict()

            if (
                gatepass["application_id"]
                == application_id
            ):
                return gatepass

        return None

    def update_gatepass_status(
            self,
            gatepass_id: str,
            status: str
    ):
        self.db.collection(
            "gate_passes"
        ).document(
            gatepass_id
        ).update(
            {
                "status": status
            }
        )

        return {
            "gatepass_id": gatepass_id,
            "status": status
        }

    def count_active_gatepasses(self):

        docs = self.db.collection(
            "gate_passes"
        ).stream()

        count = 0

        for doc in docs:

            gatepass = doc.to_dict()

            if gatepass["status"] == "ACTIVE":
                count += 1

        return count

    