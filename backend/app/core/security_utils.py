from backend.app.core.constans import SECURITY_STATUS, SAFETY_TIPS, VULNERABILITY_SCORES, COLOR_SECURITY_STATUS
from backend.app.schemas import SecurityStatus, PasswordVulnerabilities

from typing import List

def get_vulnerabilty_scores(vulnerability: PasswordVulnerabilities) -> int:
    """Find the security score assigned to the vulnerability found.
    
    Args:
        vulnerability (PasswordVulnerabilities): Vulnerability for which a score is sought

    Returns:
        vulnerability security score
    """
    return VULNERABILITY_SCORES.get(vulnerability, 0)

def get_vulnerabilities(detected_vulnerabilities: List[PasswordVulnerabilities]) -> List[str]:
    """Find the string value of the detected vulnerabilities.

    Args:
        detected_vulnerabilities (List[PasswordVulnerabilities]): List of vulnerabilities whose str value will be found.

    Returns:
        List of vulnerabilities in str.
    """
    vulnerabilities = [v.value for v in detected_vulnerabilities]    
    
    return vulnerabilities

def get_safety_tips(detected_vulnerabilities: List[PasswordVulnerabilities]) -> List[str]:
    """Find security tips for each vulnerability detected.

    Args:
        detected_vulnerabilities (List[PasswordVulnerabilities]): List of vulnerabilities detected.

    Returns:
        List of tips to improve the security of the provided password.
    """
    tips = [SAFETY_TIPS.get(v, "Sin sugerencias") for v in detected_vulnerabilities]
    
    return tips

def get_security_status(detected_vulnerabilities: List[PasswordVulnerabilities], default_status: SecurityStatus) -> str:
    """Find a security status for provided password.

    Args:
        detected_vulnerabilities (List[PasswordVulnerabilities]): List of vulnerbailities detected.
        default_status (SecurityStatus): default security state.

    Raises:
        RuntimeError: If the total vulnerability score is zero, it means that no vulnerabilities 
        were assessed and a status cannot be assigned.

    Returns:
        Security status assigned to the provided password.
    """
    safety_score = sum(get_vulnerabilty_scores(v) for v in detected_vulnerabilities)
    if safety_score == 0:
        raise RuntimeError("A status security cannot be assigned to the password")
    
    for score, status in SECURITY_STATUS:
        
        if score <= safety_score:
            return status.value
        
    return default_status.value

def get_color_security_status(secutiry_status: str | SecurityStatus) -> str:
    """Assigns a color to the provided password according to its security level.

    Args:
        secutiry_status (str | SecurityStatus): Security status of the password

    aises:
        ValueError: If the provided status does not match any value
                    defined in the SecurityStatus enum.

    Returns:
        A string representing the CSS color associated with the
        security status. Defaults to 'red' if the status has no
        color mapping.
    """
    try:
        status = SecurityStatus(secutiry_status)
    except ValueError:
        raise ValueError("The security status is not found in the registry")
    
    return COLOR_SECURITY_STATUS.get(status, "red")
    