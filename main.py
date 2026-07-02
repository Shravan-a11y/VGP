from fastapi import FastAPI
from app.core.config import settings
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.visitor_application import (
    router as visitor_application_router
)


from app.routes.gate_pass import(
    router as gate_pass_router
)

from app.routes.access_log import (
    router as access_log_router
)

from app.routes.department import (
    router as department_router
)

from app.routes.employee import(
    router as employee_router
)

from app.routes.dashboard import (
    router as dashboard_router
)

from app.routes.audit_log import(
    router as audit_log_router
)

from app.routes.frontend import(
    router as frontend_router
)



app=FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
    )

app.add_middleware(
    SessionMiddleware,
    secret_key="visitor-management-secret"
)


app.include_router(auth_router)
app.include_router(visitor_application_router)
app.include_router(gate_pass_router)
app.include_router(access_log_router)
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(dashboard_router)
app.include_router(audit_log_router)
app.include_router(frontend_router)
@app.get("/")
async def root():
    return  {
    "Message":"Visitor gate Passing"
    }



app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)