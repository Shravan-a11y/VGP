from app.core.firebase import initialize_firebase

class VisitorApplicationRepository:
    def __init__(self):
        self.db=initialize_firebase()

    def create_application(
            self,
            application_data:dict
    ):
        self.db.collection(
            "visitor_applications"
        ).document(
            application_data["application_id"]
        ).set(application_data)

        return application_data

    def get_application_by_id(
            self,
            application_id:str
    ):
        doc=self.db.collection(
            "visitor_applications"
        ).document(
            application_id
        ).get()


        if doc.exists:
            return doc.to_dict()

        return None

    def get_all_applications(self):
        docs = self.db.collection(
            "visitor_applications"
        ).stream()

        applications = []

        for doc in docs:
                applications.append(doc.to_dict())

        return applications

    def get_pending_applications_by_hod(
        self,
        employee_id: str
    ):
        docs = self.db.collection(
        "visitor_applications"
        ).stream()

        applications = []

        for doc in docs:

            application = doc.to_dict()

            if (
            application["host_id"] == employee_id
            and application["status"] == "PENDING"
            ):
                applications.append(
                application
            )

        return applications
    
    def update_application_status(
              self,
              application_id:str,
              status:str,
        ):
         self.db.collection(
              "visitor_applications"
         ).document(
              application_id
         ).update(
             { 
                  "status":status
             }
         )
         return  {
                  "application_id": application_id,
                   "status":status,
              }


    def get_applications_by_hod(
        self,
        employee_id: str
    ):
        docs = self.db.collection(
            "visitor_applications"
        ).stream()

        applications = []

        for doc in docs:

            application = doc.to_dict()

            if application["host_id"] == employee_id:
                applications.append(
                    application
                )

        return applications

    def count_applications(self):
        docs = self.db.collection(
            "visitor_applications"
        ).stream()

        return len(list(docs))

    def get_applications_by_phone(
    self,
    phone: str
    ):

        docs = self.db.collection(
            "visitor_applications"
        ).stream()

        applications = []

        for doc in docs:

            application = doc.to_dict()

            if application["visitor_phone"] == phone:
                applications.append(
                    application
                )

        return applications

    def search_applications(
    self,
    search: str
    ):

        docs = self.db.collection(
            "visitor_applications"
        ).stream()

        applications = []

        search = search.lower()

        for doc in docs:

            application = doc.to_dict()

            if (
                search in application["visitor_name"].lower()
                or search in application["visitor_phone"]
            ):

                applications.append(
                    application
                )

        return applications

    def filter_by_department(
    self,
    department_id: str
    ):

        docs = self.db.collection(
            "visitor_applications"
        ).stream()

        applications = []

        for doc in docs:

            application = doc.to_dict()

            if (
                application["department_id"]
                == department_id
            ):

                applications.append(
                    application
                )

        return applications