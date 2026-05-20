from backend.app.schemas import PasswordBase, PasswordAnalyzed, PasswordVulnerabilities, PasswordAnalysisCreate
from backend.app.schemas import UserResponse, UserCreate
from backend.app.models import User

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import List


class IPasswordHasher(ABC):
    
    @abstractmethod
    def hash(self, password: str) -> str: ...
    
    @abstractmethod
    def verify_password(self, plain_password: str, hasched_password: str) -> bool: ...

class IPasswordAnalyzer(ABC):
    """
    This is a interface for a password analizer.
    
    Any class that implements this interface must define the 'analyze' method.
    
    Methods:
        analyze(password: PasswordData) -> PasswordAnalyzed
        
            Analyzes a provided password and returns raw data (Booleans True-False)  which contain information about the password's security.
    """
    @abstractmethod
    def analyze(self, password: PasswordBase) -> PasswordAnalyzed: ...
    
class IVulnerabilityDetector(ABC):
    """
    This is a interface for detecting security vulnerabilities in a password.
    
    Any class that implements this interface must define the 'detect' method.
    
    Methods:
        detect(raw_data: PasswordAnalyzed, default_vulnerabilty_value: PasswordVulnerabilities) -> List[PasswordVulnerabilities]

            It detects password security vulnerabilities based on raw data (true-false booleans) which contain information about the analyzed password.
    """
    @abstractmethod
    def detect(self, raw_data: PasswordAnalyzed, default_vulnerabilty_value: PasswordVulnerabilities) -> List[PasswordVulnerabilities]:...

class IPasswordSecurityService(ABC):
    
    @abstractmethod
    def password_analyze(self, password: str) -> PasswordAnalysisCreate: ...

class ISqlRepository(ABC):
    
    @abstractmethod
    def get_user_by_email(self, db: Session, email: EmailStr) -> User | None: ...
    
    @abstractmethod
    def get_user(self, db: Session, username: str) -> User | None:...
    
    @abstractmethod
    def create_user(self, db: Session, user_data: UserCreate) -> UserResponse:...
    
    @abstractmethod
    def update_user(self, db: Session, username: str, user_data: UserCreate) -> UserResponse: ...
    
    @abstractmethod
    def add_password_analysis(self, db: Session, user_name: str, analysis_data: PasswordAnalysisCreate) -> bool: ...