from core.constans import SECURITY_STATUS, SAFETY_TIPS, VULNERABILITY_SCORES, COLOR_SECURITY_STATUS
from schemas import SecurityStatus, PasswordVulnerabilities

from typing import List

def get_vulnerabilty_scores(vulnerability: PasswordVulnerabilities) -> int:
    return VULNERABILITY_SCORES.get(vulnerability, 0)

async def get_vulnerabilities(detected_vulnerabilities: List[PasswordVulnerabilities]) -> List[str]:
    vulnerabilities = [v.value for v in detected_vulnerabilities]    
    
    return vulnerabilities

async def get_safety_tips(detected_vulnerabilities: List[PasswordVulnerabilities]) -> List[str]:
    tips = [SAFETY_TIPS.get(v, "Sin sugerencias") for v in detected_vulnerabilities]
    
    return tips

async def get_security_status(detected_vulnerabilities: List[PasswordVulnerabilities], default_status: SecurityStatus) -> str:
    safety_score = sum(get_vulnerabilty_scores(v) for v in detected_vulnerabilities)
    if safety_score == 0:
        raise RuntimeError("A status security cannot be assigned to the password")
    
    for score, status in SECURITY_STATUS:
        
        if score <= safety_score:
            return status.value
        
    return default_status.value

async def get_color_security_status(secutiry_status: str | SecurityStatus) -> str:
    try:
        status = SecurityStatus(secutiry_status)
    except ValueError:
        raise ValueError("The security status is not found in the registry")
    
    return COLOR_SECURITY_STATUS.get(status, "red")
    