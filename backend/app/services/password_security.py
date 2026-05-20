from backend.app.schemas import PasswordBase, PasswordAnalysisCreate, PasswordVulnerabilities, SecurityStatus
from backend.app.core import (
    IPasswordAnalyzer, IPasswordSecurityService, IVulnerabilityDetector,
    get_color_security_status, get_safety_tips, get_security_status,
    get_vulnerabilities
)

class PasswordSecurityService(IPasswordSecurityService):
    def __init__(self, password_analyzer: IPasswordAnalyzer, vulnerability_detector: IVulnerabilityDetector):
        self.password_analyzer = password_analyzer
        self.vulnerability_detector = vulnerability_detector
        
    def password_analyze(self, password: PasswordBase, default_vulnerabilty_value: PasswordVulnerabilities, default_security_status: SecurityStatus) -> PasswordAnalysisCreate:
        raw_data = self.password_analyzer.analyze(password)
        detected_vulnerabilities = self.vulnerability_detector.detect(raw_data, default_vulnerabilty_value)
        security_status = get_security_status(detected_vulnerabilities, default_security_status)
        return PasswordAnalysisCreate(
            password=password.password,
            security_status= get_security_status(detected_vulnerabilities, default_security_status),
            safety_color= get_color_security_status(security_status),
            vulnerabilities=get_vulnerabilities(detected_vulnerabilities),
            feedback=get_safety_tips(detected_vulnerabilities)
        )