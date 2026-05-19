from backend.app.exceptions import EmailAlreadyExistsError, UserDoesNotExistsError
from backend.app.schemas import UserCreate, UserResponse, PasswordAnalysisCreate
from backend.app.models import User, PasswordAnalyzed
from backend.app.core import IPasswordHasher, ISqlRepository

from sqlalchemy.orm import Session
from pydantic import EmailStr
import logging
import json

logger = logging.getLogger(__name__)

class PostgreSqlRepository(ISqlRepository):
    def __init__(self, password_hasher: IPasswordHasher):
        self.password_hasher = password_hasher
    
    def get_user_by_email(self, db: Session, email: EmailStr) -> User | None:
        return db.query(User).filter(User.email == email).first()
    
    def get_user(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def create_user(self, db: Session, user_data: UserCreate) -> bool:
        password_hashed = self.password_hasher.hash(user_data.password_hash)
        
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
            logger.critical(f"[PostgreSqlRepository]: Could not be created the user, error: {e}", exc_info=True)
            raise
    
    def update_user(self, db: Session, username: str, user_data: UserCreate) -> User:
        user_db = self.get_user(db, user_data.user_name)
        if not user_db:
            logger.warning(f"The user {username} does not exist.")
            raise UserDoesNotExistsError(f"The user {username} could not be found")
        
        for key, value in user_data.model_dump().items():
            setattr(user_db, key, value)
        
        db.commit()
        db.refresh(user_db)
        
        return user_db
    
    def add_password_analysis(self, db: Session, user_name: str, analysis_data: PasswordAnalysisCreate) -> bool:
        user_db = self.get_user(db, user_name)
        if not user_db:
            raise UserDoesNotExistsError(f"The user {user_name} does not exist.")
        
        new_analysis_db = PasswordAnalyzed(
            user_id=user_db.id,
            security_score=analysis_data.security_score,
            security_status=analysis_data.security_status,
            vulnerabilities=json.dumps(analysis_data.vulnerabilities),
            feedback=json.dumps(analysis_data.feedback)
        )
        try:
            db.add(new_analysis_db)
            db.commit()
            return True
        except Exception as e:
            logger.critical(f"""[PostrgreSqlReposiroty]: An error occurred while inserting the 
                password analysis into the database for user with ID {user_db.id}. Error: {e}
            """, exc_info=True)
            db.rollback()
            raise
        
        
        
        