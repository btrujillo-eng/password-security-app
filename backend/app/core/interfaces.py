from schemas import PasswordData, PasswordAnalyzed, PasswordVulnerabilities, PasswordResponse
from schemas import UserResponse, UserData, IdModel

from abc import ABC, abstractmethod
from typing import List


class IPasswordAnalyzer(ABC):
    """
    This is a interface for a password analizer.
    
    Any class that implements this interface must define the 'analyze' method.
    
    Methods:
        analyze(password: PasswordData) -> PasswordAnalyzed
        
            Analyzes a provided password and returns raw data (Booleans True-False)  which contain information about the password's security.
    """
    @abstractmethod
    async def analyze(self, password: PasswordData) -> PasswordAnalyzed: ...
    
class IVulnerabilityDetector(ABC):
    """
    This is a interface for detecting security vulnerabilities in a password.
    
    Any class that implements this interface must define the 'detect' method.
    
    Methods:
        detect(raw_data: PasswordAnalyzed, default_vulnerabilty_value: PasswordVulnerabilities) -> List[PasswordVulnerabilities]

            It detects password security vulnerabilities based on raw data (true-false booleans) which contain information about the analyzed password.
    """
    @abstractmethod
    async def detect(self, raw_data: PasswordAnalyzed, default_vulnerabilty_value: PasswordVulnerabilities) -> List[PasswordVulnerabilities]:...

class IPasswordSecurityService(ABC):
    
    @abstractmethod
    async def password_analyze(self, password: str) -> PasswordResponse: ...

class IUserRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[UserResponse]: ...
    
    @abstractmethod
    def get_user_by_id(self, id: IdModel) -> UserResponse:...
    
    @abstractmethod
    def create(self, user_data: UserData) -> UserResponse:...
    
    @abstractmethod
    def create_many(self, users: List[UserData]) -> bool: ...
    
    @abstractmethod
    def update(self, id: IdModel, user_data: UserData) -> UserResponse: ...
    
    @abstractmethod
    def delete(self, id: IdModel) -> bool: ...