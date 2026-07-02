from fastapi import APIRouter,Depends

from app.core.dependencies import get_current_user,require_hod

from app.services.visitor_application_service import(
    VisitorApplicationService
)
from app.models.visitor_application import VisitorApplicationCreate


router = APIRouter(
    prefix="/visitor-applications",
    tags=["Visitor Applications"]
)

service = VisitorApplicationService()

@router.post("/")
async def create_application(
    application_data: VisitorApplicationCreate,
    current_user=Depends(get_current_user)
):

    print("APPLICATION DATA:", application_data)
    print("TYPE:", type(application_data))
    print("CURRENT USER:", current_user)

    application = service.submit_application(
        application_data,
        current_user
    )

    return application



@router.get("/")
async def get_all_applications(
      current_user=Depends(get_current_user)
):
      return service.get_all_applications()


@router.get("/pending")
async def get_pending_applications(
    current_user=Depends(
        require_hod
    )
):
    return service.get_pending_applications_for_hod(
        current_user["employee_id"]
    )

@router.get("/{application_id}")
async def get_application_by_id(
    application_id:str,
    current_user=Depends(get_current_user)
    ):
        application=service.get_application_by_id(
        application_id
    )

        return 

@router.put("/{application_id}/approve")
async def approve_application(
      application_id:str,
      current_user=Depends(require_hod)
    ):

      
      return service.approve_application(
            application_id,
            current_user
      )

@router.put("/{application_id}/reject")
async def reject_application(
      application_id:str,
      current_user=Depends(require_hod)
    ):
      return service.reject_application(
            application_id
      )


