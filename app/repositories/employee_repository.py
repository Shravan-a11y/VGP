from app.core.firebase import initialize_firebase

class EmployeeRepository:

    def __init__(self):
        self.db=initialize_firebase()


    def create_employee(
            self,
            employee_data:dict
    ):
        self.db.collection(
            "employees"
        ).document(
            employee_data["employee_id"]
        ).set(
            employee_data
        )

        return employee_data


    def get_employee_by_id(
            self,
            employee_id:str
    ):

        doc=self.db.collection(
            "employees"
        ).document(
            employee_id
        ).get()

        if doc.exists :
            return doc.to_dict()

        return None


    def get_all_employees(
            self,
    ):
        docs=self.db.collection(
            "employees"
        ).stream()

        employees=[]

        for doc in docs:
            employees.append(
                doc.to_dict()
            )

        return employees

    def get_hod_by_department(

            self,
            depatment_id:str
    ):
        docs=self.db.collection(
            "employees"
        ).stream()

        for doc in docs:

            employee=doc.to_dict()

            if(
                employee["department_id"]==depatment_id
                and employee["role"]=="HOD"
            ):
                return employee

        return None

    def count_employees(self):
        docs = self.db.collection(
            "employees"
        ).stream()

        return len(list(docs))

    def update_employee(
    self,
    employee_id: str,
    employee_data: dict
    ):

        self.db.collection(
            "employees"
        ).document(
            employee_id
        ).update(
            employee_data
        )

        return self.get_employee_by_id(
            employee_id
        )
            
