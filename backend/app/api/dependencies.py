from backend.app.services import PasswordAnalyzer, PasswordSecurityService, VulnerabilityDetector
from backend.app.schemas import PasswordVulnerabilities, SecurityStatus
from backend.app.crud import PostgreSqlRepository
from backend.app.core import PasswordHasher
from backend.app.database import SessionLocal

def get_password_analyzer() -> PasswordAnalyzer:
    return PasswordAnalyzer()

def get_vulnerability_detector() -> VulnerabilityDetector:
    return VulnerabilityDetector()

def get_password_security_service() -> PasswordSecurityService:
    return PasswordSecurityService(get_password_analyzer(), get_vulnerability_detector())

def get_default_vulnerabilty_value() -> PasswordVulnerabilities:
    return PasswordVulnerabilities.WITHOUT_VULNERABILITIES

def get_default_security_status() -> SecurityStatus:
    return SecurityStatus.UNSAFE

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_user_repository() -> PostgreSqlRepository:
    return PostgreSqlRepository(get_password_hasher())

def get_session_db():
    db_session = SessionLocal()
    
    try:
        
        yield db_session
    finally:
        db_session.close()