from schemas import PasswordData, PasswordResponse, PasswordVulnerabilities, SecurityStatus
from core import (
    IPasswordAnalyzer, IPasswordSecurityService, IVulnerabilityDetector,
    get_color_security_status, get_safety_tips, get_security_status,
    get_vulnerabilities
)

class PasswordSecurityService(IPasswordSecurityService):
    def __init__(self, password_analyzer: IPasswordAnalyzer, vulnerability_detector: IVulnerabilityDetector):
        self.password_analyzer = password_analyzer
        self.vulnerability_detector = vulnerability_detector
        
    async def password_analyze(self, password: PasswordData, default_vulnerabilty_value: PasswordVulnerabilities, default_security_status: SecurityStatus) -> PasswordResponse:
        raw_data = await self.password_analyzer.analyze(password)
        detected_vulnerabilities = await self.vulnerability_detector.detect(raw_data, default_vulnerabilty_value)
        return PasswordResponse(
            password=password.password,
            status= await get_security_status(detected_vulnerabilities, default_security_status),
            color= await get_color_security_status(await get_security_status(detected_vulnerabilities, default_security_status)),
            vulnerabilities=await get_vulnerabilities(detected_vulnerabilities),
            tips=await get_safety_tips(detected_vulnerabilities)
        )
        

