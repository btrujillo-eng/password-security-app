from backend.app.api.dependencies import get_password_security_service, get_default_vulnerabilty_value, get_default_security_status
from backend.app.schemas import PasswordBase, PasswordAnalysisCreate, PasswordVulnerabilities, SecurityStatus
from backend.app.services import PasswordSecurityService

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/password/check", tags=["analyze password security"])

@router.post("/", response_model=PasswordAnalysisCreate)
async def analyze_password_security(
    password: PasswordBase,
    password_security_service: PasswordSecurityService = Depends(get_password_security_service),
    default_vulnerabilty_value: PasswordVulnerabilities = Depends(get_default_vulnerabilty_value),
    default_security_status: SecurityStatus = Depends(get_default_security_status)
    ):
    
    return await password_security_service.password_analyze(password, default_vulnerabilty_value, default_security_status)