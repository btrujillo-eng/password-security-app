from backend.app.schemas import PasswordBase, PasswordAnalyzed, PasswordVulnerabilities, PasswordAnalysisCreate
from backend.app.schemas import UserResponse, UserCreate
from backend.app.models import User

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import List

class IPasswordHasher(ABC):
    """Interface for a password hashing operations.
    
    Any clas that implement this interface must define the 'hash' and 'verify_password' methods.    
    """
    @abstractmethod
    def hash(self, password: str) -> str:
        """Hashes a plain text password using bcrypt with an auto-generated salt.

        Args:
            password (str): The plain text password to hasher.

        Returns:
            The hashed password as a 'UTF-8' enconded string.
        """
        ...
    
    @abstractmethod
    def verify_password(self, plain_password: str, hasched_password: str) -> bool: 
        """Verifies a plain text password against a hashed one.

        Args:
            plain_password: The plain text password provided by the user.
            hashed_password: The stored hashed password to compare against.

        Returns:
            True if the passwords match, False otherwise.
        """
        ...

class IPasswordAnalyzer(ABC):
    """Interface for a password analizer.
    
    Any class that implements this interface must define the 'analyze' method.
    """
    @abstractmethod
    def analyze(self, password: PasswordBase) -> PasswordAnalyzed:
        """Analyzes the security of a provided password.

        Args:
            password (PasswordBase): Password that will be subject to security analysis

        Returns:
            Raw data (Booleans True-False) which contain information about
                the password.
        """
        ...
    
class IVulnerabilityDetector(ABC):
    """Interface for detecting security vulnerabilities in a password.
    
    Any class that implements this interface must define the 'detect' method.
    """
    @abstractmethod
    def detect(self, raw_data: PasswordAnalyzed, default_vulnerabilty_value: PasswordVulnerabilities) -> List[PasswordVulnerabilities]:
        """It detects password security vulnerabilities based on raw data (true-false booleans) which contain information about the analyzed password.
        Args:
            raw_data (PasswordAnalyzed): Raw data used to find vulnerabilities in the prvided password.
            default_vulnerabilty_value (PasswordVulnerabilities): Vulnerability default value.

        Returns:
            List[PasswordVulnerabilities]: List of vulnerabities found in the provided password.
        """
        ...

class IPasswordSecurityService(ABC):
    """Interface for the password security service.
    
    Any class tthat implement this interface must define 'password_analyze' method.
    """
    
    @abstractmethod
    def password_analyze(self, password: str) -> PasswordAnalysisCreate: 
        """It analyzes the security status of the provided password.

        Args:
            password (str): Passoword to analyze.

        Returns:
            PasswordAnalysisCreate: Summary about the status security of the porvided password.
        """
        ...

class ISqlRepository(ABC):
    """Interface for a SQL repository.
    """
    
    @abstractmethod
    def get_user_by_email(self, db: Session, email: EmailStr) -> User | None: 
        """Retrieves a user from the database by their email address.

        Args:
            db: Active SQLAlchemy database session.
            email: The email address to search for.

        Returns:
            The User instance if found, or None if no user
            exists with the provided email.
        """
        ...
    
    @abstractmethod
    def get_user(self, db: Session, username: str) -> User | None:
        """Retrieves a user from the database by their username.

        Args:
            db (Session): Active SQLAlchemy database session.
            username (str): The username to search for.

        Returns:
            The User instance if found, or None if no user
            exists with the provided username.
        """
        ...
    
    @abstractmethod
    def create_user(self, db: Session, user_data: UserCreate) -> UserResponse:
        """Creates a new user in the database with a hashed password.

        Args:
            db (Session): Active SQLAlchemy database session.
            user_data (UserCreate): Pydantic schema containing the new user's
                   username, email, and plain text password
        
        Returns:
            True if the user was created and committed successfully.
        """
        ...
    
    @abstractmethod
    def update_user(self, db: Session, username: str, user_data: UserCreate) -> UserResponse: 
        """Updates an existing user's data in the database.

        Args:
            db (Session): Active SQLAlchemy database session.
            username (str): The username of the user to update.
            user_data (UserCreate): Pydantic schema containing the updated
                   user fields to apply.

        Returns:
            The updated User instance refreshed from the database.
        """
        ...
    
    @abstractmethod
    def add_password_analysis(self, db: Session, user_name: str, analysis_data: PasswordAnalysisCreate) -> bool: ...