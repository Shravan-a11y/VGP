from fastapi import APIRouter, Request,Query,HTTPException,Depends
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse,Response
from datetime import date
from app.services.auth_service import login_user
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import (
    DepartmentRepository
)

from app.repositories.employee_repository import (
    EmployeeRepository
)

from app.repositories.visitor_application_repository import (
    VisitorApplicationRepository
)

from app.repositories.visitor_application_repository import (
    VisitorApplicationRepository
)

from app.services.visitor_application_service import (
    VisitorApplicationService
)

from app.models.visitor_application import (
    VisitorApplicationCreate
)

from app.repositories.gate_pass_repository import (
    GatePassRepository
)

from app.services.employee_service import(
    EmployeeService
)
from app.repositories.access_log_repository import (
    AccessLogRepository
)

from app.models.employee import (
    EmployeeCreate
)
from app.models.department import(
    DepartmentCreate
)

from app.services.department_service import (
    DeparmentService
)

from app.repositories.audit_log_repository import (
    AuditLogRepository
)

from app.services.report_service import(
    ReportService
)
from app.core.session_dependencies import(
    require_admin,
    require_guard,
    require_hod
)

router = APIRouter()

# jinja 2 Templating
templates = Jinja2Templates(
    directory="app/templates"
)

from app.utils.template_filter import (
    format_datetime
)

templates.env.filters[
    "datetime"
] = format_datetime



user_repository=UserRepository()
department_repository = DepartmentRepository()
employee_repository = EmployeeRepository()
visitor_repository = VisitorApplicationRepository()
application_service = VisitorApplicationService()
gatepass_repository = GatePassRepository()
employee_service=EmployeeService()
access_log_repository = AccessLogRepository()
department_service = DeparmentService()
audit_log_repository = AuditLogRepository()
report_service=ReportService()

@router.get("/")
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "request": request
        }
    )


@router.post("/login")
async def login_submit(
    request:Request,
    email: str = Form(...),
    password: str = Form(...),
    
):
    print("LOGIN ROUTE HIT")

    token = login_user(
        email,
        password
    )

    print("EMAIL:", email)
    print("TOKEN:", token)

    if not token:
        return RedirectResponse(
            "/",
            status_code=302
        )

    user = user_repository.get_user_by_email(
        email
    )

    print("USER:", user)

    request.session["user"] = {
    "user_id": user["user_id"],
    "employee_id": user["employee_id"],
    "role": user["role"],
    "email": user["email"]
    }

    print("SESSION USER:", request.session["user"])

    role = user["role"]

    if role == "ADMIN":
        return RedirectResponse(
            "/admin/dashboard",
            status_code=302
        )

    elif role == "HOD":
        return RedirectResponse(
            "/hod/dashboard",
            status_code=302
        )

    elif role == "GUARD":
        return RedirectResponse(
            "/guard/dashboard",
            status_code=302
        )

    return RedirectResponse(
        "/",
        status_code=302
    )


@router.get("/admin/dashboard")
async def admin_dashboard(
    request: Request,
    search: str = "",
    department_id: str = "",
    current_user=Depends(require_admin)
):

    total_departments = (
        department_repository.count_departments()
    )

    total_employees = (
        employee_repository.count_employees()
    )

    total_applications = (
        visitor_repository.count_applications()
    )

    active_gatepasses = (
        gatepass_repository.count_active_gatepasses()
    )

    departments = (
        department_repository.get_all_departments()
    )

    applications = (
        visitor_repository.get_all_applications()
    )

    # Department Filter
    
    if department_id:

        applications = [

            app

            for app in applications

            if app.get("department_id") == department_id

        ]

    # Search Filter
    if search:

        applications = [

            app

            for app in applications

            if (

                search.lower()
                in app["visitor_name"].lower()

                or

                search
                in app["visitor_phone"]

            )

        ]

    pending = 0
    approved = 0
    rejected = 0

    for application in applications:

        if application["status"] == "PENDING":
            pending += 1

        elif application["status"] == "APPROVED":
            approved += 1

        elif application["status"] == "REJECTED":
            rejected += 1

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "request": request,

            "search": search,
            "department_id": department_id,

            "departments": departments,

            "applications": applications,

            "total_departments": total_departments,
            "total_employees": total_employees,
            "total_applications": total_applications,
            "active_gatepasses": active_gatepasses,

            "pending": pending,
            "approved": approved,
            "rejected": rejected
        }
    )
@router.get("/hod/dashboard")
async def hod_dashboard(
    request: Request,
    search: str = "",
    status: str = "",
    current_user=Depends(require_hod)
):
    

    current_user = request.session.get(
        "user"
    )

    all_applications = (
        visitor_repository.get_all_applications()
    )

    applications = []

    # Only applications for this HOD
    for app in all_applications:

        if (
            app["host_id"]
            == current_user["employee_id"]
        ):
            applications.append(app)

    # Search Filter
    if search:

        applications = [

            app

            for app in applications

            if (

                search.lower()
                in app["visitor_name"].lower()

                or

                search
                in app["visitor_phone"]

            )

        ]

    # Status Filter
    if status:

        applications = [

            app

            for app in applications

            if app["status"] == status

        ]

    pending_count = 0
    approved_count = 0
    rejected_count = 0

    for app in applications:

        if app["status"] == "PENDING":
            pending_count += 1

        elif app["status"] == "APPROVED":
            approved_count += 1

        elif app["status"] == "REJECTED":
            rejected_count += 1

    return templates.TemplateResponse(
        request=request,
        name="hod/dashboard.html",
        context={
            "request": request,

            "pending_count": pending_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count,

            "applications": applications,

            "search": search,
            "status": status,

            "total_requests": len(applications)
        }
    )
@router.post("/hod/approve/{application_id}")
async def approve_application(
    application_id: str,
    request:Request,
    current_user=Depends(require_hod)
):

    current_user = request.session.get(
    "user"
)

    application_service.approve_application(
        application_id,
        current_user
    )

    return RedirectResponse(
        "/hod/dashboard",
        status_code=302
    )


@router.post("/hod/reject/{application_id}")
async def reject_application(
    application_id: str,
    request:Request,
    current_user=Depends(require_hod)
):

    current_user = request.session.get(
    "user"
)

    application_service.reject_application(
        application_id,
        current_user
    )

    return RedirectResponse(
        "/hod/dashboard",
        status_code=302
    )


from app.services.access_log_service import (
    AccessLogService
)

access_service = AccessLogService()


@router.get("/guard/dashboard")
async def guard_dashboard(
    request: Request,
    current_user=Depends(require_guard)
):

    access_logs = (
        access_log_repository.get_all_logs()
    )

    total_entries = 0
    total_exits = 0

    for log in access_logs:

        if log["action"] == "ENTRY":
            total_entries += 1

        elif log["action"] == "EXIT":
            total_exits += 1

    visitors_inside = (
        total_entries
        -
        total_exits
    )

    recent_logs = sorted(

        access_logs,

        key=lambda x: x["timestamp"],

        reverse=True

    )[:5]

    return templates.TemplateResponse(

        request=request,

        name="guard/dashboard.html",

        context={

            "request": request,

            "total_entries": total_entries,

            "total_exits": total_exits,

            "visitors_inside": visitors_inside,

            "recent_logs": recent_logs

        }

    )

@router.post("/guard/entry")
async def guard_entry(
    gatepass_id: str = Form(...),
    current_user=Depends(require_guard)
):

    access_service.record_entry(
        gatepass_id
    )

    return RedirectResponse(
        "/guard/dashboard",
        status_code=302
    )

@router.post("/guard/exit")
async def guard_exit(
    gatepass_id: str = Form(...),
    current_user=Depends(require_guard)
):

    access_service.record_exit(
        gatepass_id
    )

    return RedirectResponse(
        "/guard/dashboard",
        status_code=302
    )


@router.get("/guard/process/{gatepass_id}")
async def process_qr_scan(
    gatepass_id: str,
    current_user=Depends(require_guard)
):

    logs = access_log_repository.get_logs_by_gatepass(
        gatepass_id
    )

    has_entry = any(
        log["action"] == "ENTRY"
        for log in logs
    )

    has_exit = any(
        log["action"] == "EXIT"
        for log in logs
    )

    if not has_entry:

        access_service.record_entry(
            gatepass_id
        )

        return {
            "action": "ENTRY",
            "message": "Entry Recorded Successfully"
        }

    elif has_entry and not has_exit:

        access_service.record_exit(
            gatepass_id
        )

        return {
            "action": "EXIT",
            "message": "Exit Recorded Successfully"
        }

    raise HTTPException(
        status_code=400,
        detail="Gate Pass Already Used"
    )

@router.get("/visitor/apply")
async def visitor_form(
    request: Request
):

    departments = (
        department_repository
        .get_all_departments()
    )

    print("DEPARTMENTS:", departments)

    return templates.TemplateResponse(
        request=request,
        name="visitor/apply.html",
        context={
            "request": request,
            "departments": departments
        }
    )

@router.post("/visitor/apply")
async def submit_visitor_application(
    visitor_name: str = Form(...),
visitor_email: str = Form(...),
visitor_phone: str = Form(...),
purpose: str = Form(...),
visit_date: date = Form(...),
expected_time: str = Form(...),
department_id: str = Form(...)
):

    application_data = VisitorApplicationCreate(
    visitor_name=visitor_name,
    visitor_email=visitor_email,
    visitor_phone=visitor_phone,
    purpose=purpose,
    visit_date=visit_date,
    expected_time=expected_time,
    department_id=department_id
)

    current_user = {
        "user_id": "visitor"
    }

    application = (
        application_service.submit_application(
            application_data,
            current_user
        )
    )

    return RedirectResponse(
        f"/visitor/status/{application['application_id']}",
        status_code=302
    )

@router.get("/visitor/success")
async def visitor_success(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="visitor/success.html",
        context={
            "request": request
        }
    )


@router.get("/visitor/status")
async def visitor_status_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="visitor/status.html",
        context={
            "request": request,
            "applications": []
        }
    )

@router.post("/visitor/status")
async def visitor_status_search(
    request: Request,
    visitor_phone: str = Form(...)
):

    applications = (
        visitor_repository
        .get_applications_by_phone(
            visitor_phone
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="visitor/status.html",
        context={
            "request": request,
            "applications": applications,
            "visitor_phone": visitor_phone
        }
    )

@router.get("/visitor/gatepass/{application_id}")
async def visitor_gatepass(
    request: Request,
    application_id: str
):

    gatepass = (
        gatepass_repository
        .get_gate_pass_by_application_id(
            application_id
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="visitor/gatepass.html",
        context={
            "request": request,
            "gatepass": gatepass
        }
    )

@router.get("/visitor/status/{application_id}")
async def visitor_application_status(
    request: Request,
    application_id: str
):

    application = (
        visitor_repository.get_application_by_id(
            application_id
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="visitor/application_status.html",
        context={
            "request": request,
            "application": application
        }
    )

@router.get("/visitor/gatepass/{application_id}")
async def visitor_gatepass(
    request: Request,
    application_id: str
):

    gatepass = (
        gatepass_repository
        .get_gate_pass_by_application_id(
            application_id
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="visitor/gatepass.html",
        context={
            "request": request,
            "gatepass": gatepass
        }
    )

@router.get("/guard/process/{gatepass_id}")
async def process_scan(
    request: Request,
    gatepass_id: str
):

    try:

        access_service.record_entry(
            gatepass_id
        )

        message = (
            "Entry Recorded Successfully"
        )

    except Exception as e:

        message = str(e)

    return templates.TemplateResponse(
        request=request,
        name="guard/result.html",
        context={
            "request": request,
            "message": message
        }
    )


@router.get("/admin/employees")
async def employee_management(
    request: Request,
    search: str = "",
    department_id: str = "",
    role: str = "",
    current_user=Depends(require_admin)
):

    employees = (
        employee_repository.get_all_employees()
    )

    departments = (
        department_repository.get_all_departments()
    )

    department_map = {}

    for department in departments:

        department_map[
            department["department_id"]
        ] = department["department_name"]

    for employee in employees:

        employee["department_name"] = (
            department_map.get(
                employee["department_id"],
                "Unknown"
            )
        )

    # Search Filter
    if search:

        employees = [

            employee

            for employee in employees

            if (

                search.lower()
                in employee["employee_name"].lower()

                or

                search.lower()
                in employee["employee_email"].lower()

            )

        ]

    # Department Filter
    if department_id:

        employees = [

            employee

            for employee in employees

            if employee["department_id"] == department_id

        ]

    # Role Filter
    if role:

        employees = [

            employee

            for employee in employees

            if employee["role"] == role

        ]

    return templates.TemplateResponse(
        request=request,
        name="admin/employees.html",
        context={
            "request": request,
            "employees": employees,
            "departments": departments,
            "search": search,
            "department_id": department_id,
            "role": role
        }
    )

@router.get("/admin/employee/{employee_id}")
async def view_employee(
    employee_id: str,
    request: Request,
    current_user=Depends(require_admin)
):

    employee = (
        employee_repository.get_employee_by_id(
            employee_id
        )
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    department = (
        department_repository.get_department_by_id(
            employee["department_id"]
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/view_employee.html",
        context={
            "request": request,
            "employee": employee,
            "department": department
        }
    )


@router.get("/admin/edit-employee/{employee_id}")
async def edit_employee_page(
    employee_id: str,
    request: Request,
    current_user=Depends(require_admin)
):

    employee = (
        employee_repository.get_employee_by_id(
            employee_id
        )
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    departments = (
        department_repository.get_all_departments()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/edit_employee.html",
        context={
            "request": request,
            "employee": employee,
            "departments": departments
        }
    )


@router.post("/admin/edit-employee/{employee_id}")
async def edit_employee_submit(
    employee_id: str,
    employee_name: str = Form(...),
    employee_email: str = Form(...),
    department_id: str = Form(...),
    role: str = Form(...),
    current_user=Depends(require_admin)
):

    employee_service.update_employee(
        employee_id=employee_id,
        employee_name=employee_name,
        employee_email=employee_email,
        department_id=department_id,
        role=role
    )

    return RedirectResponse(
        "/admin/employees",
        status_code=302
    )


@router.get("/admin/visitors")
async def visitor_management(
    request: Request,
    search: str = "",
    department_id: str = "",
    status: str = "",
    current_user=Depends(require_admin)
):

    applications = (
        visitor_repository.get_all_applications()
    )

    departments = (
        department_repository.get_all_departments()
    )

    # Create Department ID -> Department Name mapping
    department_map = {}

    for department in departments:

        department_map[
            department["department_id"]
        ] = department["department_name"]

    # Add department name to each application
    for application in applications:

        application["department_name"] = (
            department_map.get(
                application["department_id"],
                "Unknown"
            )
        )

    # Search Filter
    if search:

        applications = [

            app

            for app in applications

            if (

                search.lower()
                in app["visitor_name"].lower()

                or

                search.lower()
                in app["visitor_email"].lower()

                or

                search
                in app["visitor_phone"]

            )

        ]

    # Department Filter
    if department_id:

        applications = [

            app

            for app in applications

            if app["department_id"] == department_id

        ]

    # Status Filter
    if status:

        applications = [

            app

            for app in applications

            if app["status"] == status

        ]

    return templates.TemplateResponse(
        request=request,
        name="admin/visitors.html",
        context={
            "request": request,
            "applications": applications,
            "departments": departments,
            "search": search,
            "department_id": department_id,
            "status": status
        }
    )

@router.get("/admin/visitor/{application_id}")
async def view_visitor(
    application_id: str,
    request: Request,
    current_user=Depends(require_admin)
):

    application = (
        visitor_repository.get_application_by_id(
            application_id
        )
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Visitor application not found"
        )

    department = (
        department_repository.get_department_by_id(
            application["department_id"]
        )
    )

    host = (
        employee_repository.get_employee_by_id(
            application["host_id"]
        )
    )

    gatepass = (
        gatepass_repository
        .get_gate_pass_by_application_id(
            application_id
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/view_visitor.html",
        context={
            "request": request,
            "application": application,
            "department": department,
            "host": host,
            "gatepass": gatepass
        }
    )

@router.get("/admin/visitor/logs/{application_id}")
async def visitor_logs(
    application_id: str,
    request: Request,
    current_user=Depends(require_admin)
):

    application = (
        visitor_repository.get_application_by_id(
            application_id
        )
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    gatepass = (
        gatepass_repository
        .get_gate_pass_by_application_id(
            application_id
        )
    )

    logs = []

    current_status = "Gate Pass Not Generated"

    if gatepass:

        logs = (
            access_log_repository
            .get_logs_by_gatepass(
                gatepass["gatepass_id"]
            )
        )

        # Determine visitor status from access logs
        if len(logs) == 0:

            current_status = "Not Entered"

        else:

            last_log = logs[-1]

            if last_log["action"] == "ENTRY":

                current_status = "Inside Campus"

            elif last_log["action"] == "EXIT":

                current_status = "Exited Campus"

            else:

                current_status = "Unknown"

    return templates.TemplateResponse(
        request=request,
        name="admin/visitor_logs.html",
        context={
            "request": request,
            "application": application,
            "gatepass": gatepass,
            "logs": logs,
            "current_status": current_status
        }
    )

@router.get("/admin/add-employee")
async def add_employee_page(
    request: Request,
    current_user=Depends(require_admin)
):

    departments = (
        department_repository.get_all_departments()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/add_employee.html",
        context={
            "request": request,
            "departments": departments
        }
    )

@router.post("/admin/add-employee")
async def add_employee(

    employee_name: str = Form(...),
    employee_email: str = Form(...),
    department_id: str = Form(...),
    role: str = Form(...),
    current_user=Depends(require_admin)

):

    employee_data = EmployeeCreate(

        employee_name=employee_name,
        employee_email=employee_email,
        department_id=department_id,
        role=role

    )

    employee_service.create_employee(
        employee_data
    )

    return RedirectResponse(
        url="/admin/employees",
        status_code=303
    )


@router.get("/admin/departments")
async def department_management(
    request: Request,
    search: str = "",
    current_user=Depends(require_admin)
):

    departments = (
        department_repository.get_all_departments()
    )

    employees = (
        employee_repository.get_all_employees()
    )

    # Search
    if search:

        departments = [

            department

            for department in departments

            if search.lower()
            in department["department_name"].lower()

        ]

    # Employee Count
    for department in departments:

        employee_count = 0

        for employee in employees:

            if (
                employee["department_id"]
                ==
                department["department_id"]
            ):
                employee_count += 1

        department["employee_count"] = employee_count

    return templates.TemplateResponse(
        request=request,
        name="admin/departments.html",
        context={
            "request": request,
            "departments": departments,
            "search": search
        }
    )


@router.post("/admin/add-department")
async def add_department(

    department_name: str = Form(...),
    department_code: str = Form(...),
    current_user=Depends(require_admin)

):

    department_data = DepartmentCreate(

        department_name=department_name,
        department_code=department_code

    )

    department_service.create_department(
        department_data
    )

    return RedirectResponse(
        url="/admin/departments",
        status_code=303
    )

@router.get("/admin/add-department")
async def add_department_page(
    request: Request,
    current_user=Depends(require_admin)
):
    return templates.TemplateResponse(
        request=request,
        name="admin/add_department.html",
        context={
            "request": request
        }
    )

@router.get("/admin/department/{department_id}")
async def view_department(
    department_id: str,
    request: Request,
    current_user=Depends(require_admin)
):

    department = (
        department_repository.get_department_by_id(
            department_id
        )
    )

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    employees = (
        employee_repository.get_all_employees()
    )

    department_employees = []

    for employee in employees:

        if (
            employee["department_id"]
            ==
            department_id
        ):

            department_employees.append(
                employee
            )

    hod = None

    if department.get("hod_id"):

        hod = (
            employee_repository.get_employee_by_id(
                department["hod_id"]
            )
        )

    return templates.TemplateResponse(
        request=request,
        name="admin/view_department.html",
        context={
            "request": request,
            "department": department,
            "employees": department_employees,
            "hod": hod
        }
    )
@router.get("/admin/security")
async def security_dashboard(
    request: Request
):

    raw_logs = (
        access_log_repository.get_all_logs()
    )

    audit_logs = (
        audit_log_repository.get_all_logs()
    )

    access_logs = []

    total_entries = 0
    total_exits = 0

    for log in raw_logs:

        if log["action"] == "ENTRY":
            total_entries += 1

        elif log["action"] == "EXIT":
            total_exits += 1

        gatepass = (
            gatepass_repository.get_gate_pass_by_id(
                log["gatepass_id"]
            )
        )

        if not gatepass:
            continue

        application = (
            visitor_repository.get_application_by_id(
                gatepass["application_id"]
            )
        )

        if not application:
            continue

        department = (
            department_repository.get_department_by_id(
                application["department_id"]
            )
        )

        host = (
            employee_repository.get_employee_by_id(
                application["host_id"]
            )
        )

        access_logs.append(

            {

                "visitor_name":
                    application["visitor_name"],

                "department_name":
                    department["department_name"]
                    if department else "N/A",

                "host_name":
                    host["employee_name"]
                    if host else "N/A",

                "action":
                    log["action"],

                "timestamp":
                    log["timestamp"]

            }

        )

    visitors_inside = (
        total_entries
        -
        total_exits
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/security.html",
        context={
            "request": request,
            "access_logs": access_logs,
            "audit_logs": audit_logs,
            "total_entries": total_entries,
            "total_exits": total_exits,
            "visitors_inside": visitors_inside,
            "audit_events": len(audit_logs)
        }
    )

@router.get("/admin/reports")
async def reports_dashboard(
    request: Request,
    current_user=Depends(require_admin)
):

    statistics = (
        report_service
        .get_dashboard_statistics()
    )

    department_report = (
        report_service
        .department_statistics()
    )

    status_chart = (
        report_service
        .get_status_chart_data()
    )

    department_chart = (
        report_service
        .get_department_chart_data()
    )

    visitor_chart = (
        report_service
        .get_daily_visitor_chart()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/reports.html",
        context={

            "request": request,

            "statistics": statistics,

            "department_report": department_report,

            "status_chart": status_chart,

            "department_chart": department_chart,

            "visitor_chart": visitor_chart

        }
    )

@router.get("/admin/reports/export/csv")
async def export_csv(
    current_user=Depends(require_admin)
):

    csv_data = (
        report_service.export_visitors_csv()
    )

    return Response(

        content=csv_data,

        media_type="text/csv",

        headers={

            "Content-Disposition":
            "attachment; filename=visitor_report.csv"

        }

    )

@router.get("/admin/reports/export/pdf")
async def export_pdf(

    current_user=Depends(require_admin)
):

    pdf_data = (
        report_service.export_visitors_pdf()
    )

    return Response(

        content=pdf_data,

        media_type="application/pdf",

        headers={

            "Content-Disposition":
            "attachment; filename=visitor_report.pdf"

        }

    )