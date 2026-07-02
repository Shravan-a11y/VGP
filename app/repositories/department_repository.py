from app.core.firebase import(
    initialize_firebase
)


class DepartmentRepository:

    def __init__ (self):
        self.db=initialize_firebase()

    def create_department(
            self,
            department_data:dict
    ):
        self.db.collection(
            "departments"
        ).document(
            department_data["department_id"]
        ).set(
            department_data
        )

        return department_data

    def get_department_by_id(
            self,
            department_id:str
    ):

        doc=self.db.collection(
            "departments"
        ).document(
            department_id
        ).get()

        if doc.exists:
            return doc.to_dict()

        return None

    def get_all_departments(
            self,
            
    ):
        docs=self.db.collection(
            "departments"
        ).stream()

        departments=[]

        for doc in docs:

            departments.append(
                doc.to_dict()
            )

        return departments

    def count_departments(self):
        docs = self.db.collection(
            "departments"
            ).stream()

        return len(list(docs))

    def assign_hod(
        self,
        department_id: str,
        employee_id: str
    ):
        self.db.collection(
            "departments"
        ).document(
            department_id
        ).update(
            {
                "hod_id": employee_id
            }
        )

        return {
            "department_id": department_id,
            "hod_id": employee_id
        }
