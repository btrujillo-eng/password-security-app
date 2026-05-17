from api.dependencies import get_password_security_service, get_default_vulnerabilty_value, get_default_security_status
from schemas import PasswordData, PasswordResponse, PasswordVulnerabilities, SecurityStatus
from services import PasswordSecurityService

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/password/check", tags=["analyze password security"])

@router.post("/", response_model=PasswordResponse)
async def analyze_password_security(
    password: PasswordData,
    password_security_service: PasswordSecurityService = Depends(get_password_security_service),
    default_vulnerabilty_value: PasswordVulnerabilities = Depends(get_default_vulnerabilty_value),
    default_security_status: SecurityStatus = Depends(get_default_security_status)
    ):
    
    return await password_security_service.password_analyze(password, default_vulnerabilty_value, default_security_status)