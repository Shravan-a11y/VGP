from datetime import datetime
from fastapi import APIRouter,Depends
from app.core.dependencies import get_current_user
from app.services.gate_pass_service import(
    GatePassService
)

router =APIRouter(
    prefix="/gate-passes",
    tags=["Gate Passes"]
)

service=GatePassService()


@router.post("/generate/{application_id}")
async def generate_gate_pass(
    application_id: str,
    current_user=Depends(get_current_user)
):

    return service.generate_gate_pass(
        application_id
    )

@router.get("/{gatepass_id}")
async def get_gate_pass(
    gatepass_id: str,
    current_user=Depends(get_current_user)
):

    return service.gatepass_repository.get_gate_pass_by_id(
        gatepass_id
    )

@router.get(
    "/validate/{gatepass_id}")
async def validate_gate_pass(
    gatepass_id:str,
    current_user=Depends(get_current_user)
):
    return service.validate_gate_pass(
        gatepass_id
    )