from backend.app.exceptions import EmailAlreadyExistsError, UserDoesNotExistsError
from backend.app.schemas import UserCreate, PasswordAnalysisCreate
from backend.app.models import User
from backend.app.core import IPasswordHasher, ISqlRepository

from sqlalchemy.orm import Session
from pydantic import EmailStr
import logging

logger = logging.getLogger(__name__)

class PostgreSqlRepository(ISqlRepository):
    def __init__(self, password_hasher: IPasswordHasher):
        self.password_hasher = password_hasher
    
    def get_user_by_email(self, db: Session, email: EmailStr) -> User | None:
        """Retrieves a user from the database by their email address.

        Args:
            db: Active SQLAlchemy database session.
            email: The email address to search for.

        Returns:
            The User instance if found, or None if no user
            exists with the provided email.
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_user(self, db: Session, username: str) -> User | None:
        """Retrieves a user from the database by their username.

        Args:
            db (Session): Active SQLAlchemy database session.
            username (str): The username to search for.

        Returns:
            The User instance if found, or None if no user
            exists with the provided username.
        """
        return db.query(User).filter(User.username == username).first()

    def create_user(self, db: Session, user_data: UserCreate) -> bool:
        """Creates a new user in the database with a hashed password.

        Args:
            db (Session): Active SQLAlchemy database session.
            user_data (UserCreate): Pydantic schema containing the new user's
                   username, email, and plain text password

        Raises:
            EmailAlreadyExistsError: If the provided email is already
                                 registered in the database.

        Returns:
            True if the user was created and committed successfully.
        """
        password_hashed = self.password_hasher.hash(user_data.password)
        
        email_exist = self.get_user_by_email(db, user_data.email)
        if email_exist:
            raise EmailAlreadyExistsError(f"The email {user_data.email} already exists.")
        
        user = User(
            username=user_data.user_name, 
            email=user_data.email,
            password_hash=password_hashed
        ) 
        try:
            db.add(user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.critical(
            "[PostgreSQLRepository]: Database error inserting password analysis for user_id: %s. Error: %s",
            user_data.user_name, 
            str(e),
            exc_info=True
        )
            raise
    
    def update_user(self, db: Session, username: str, user_data: UserCreate) -> User:
        """Updates an existing user's data in the database.

        Args:
            db (Session): Active SQLAlchemy database session.
            username (str): The username of the user to update.
            user_data (UserCreate): Pydantic schema containing the updated
                   user fields to apply.

        Raises:
            UserDoesNotExistsError: If no user is found with the provided username.

        Returns:
            The updated User instance refreshed from the database.
        """
        user_db = self.get_user(db, user_data.user_name)
        if not user_db:
            logger.warning(f"The user {username} does not exist.")
            raise UserDoesNotExistsError(f"The user {username} could not be found")
        
        for key, value in user_data.model_dump().items():
            setattr(user_db, key, value)
        
        db.commit()
        db.refresh(user_db)
        
        return user_db
    
    # def add_password_analysis(self, db: Session, user_name: str, analysis_data: PasswordAnalysisCreate) -> bool:
    #     user_db = self.get_user(db, user_name)
    #     if not user_db:
    #         raise UserDoesNotExistsError(f"The user {user_name} does not exist.")
        
    #     analysis_details = {
    #         "vulnerabilities": analysis_data.vulnerabilities,
    #         "feedback": analysis_data.feedback
    #     }
        
    #     new_analysis_db = PasswordSecurityAnalysis(
    #         # Falta implementar la contraseña con hash para implementar el historial.
    #         user_id=user_db.id,
    #         security_status=analysis_data.security_status,
    #         details=analysis_details
    #     )
    #     try:
    #         db.add(new_analysis_db)
    #         db.commit()
    #         return True
    #     except Exception as e:
    #         logger.critical(
    #         "[PostgreSQLRepository]: Database error inserting password analysis for user_id: %s. Error: %s",
    #         user_db.id, 
    #         str(e),
    #         exc_info=True
    #         )
    #         raise
    
    def add_password_analysis(self, db: Session, user_name: str, analysis_data: PasswordAnalysisCreate) -> bool:
    
        return True