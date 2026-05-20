from backend.app.api.dependencies import get_user_repository, get_password_hasher, get_session_db
from backend.app.exceptions import EmailAlreadyExistsError, UserDoesNotExistsError
from backend.app.crud import PostgreSqlRepository
from backend.app.models import User, Base
from backend.app.schemas import UserCreate
from backend.app.database import engine

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import EmailStr

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="api/v1/user", tags=["user Repository"])

@router.get("/", response_model=User)
async def get_user(
    username: str, 
    db: Session = Depends(get_session_db), 
    repository: PostgreSqlRepository = Depends(get_user_repository)
    ) -> User:
    user = repository.get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario {username} no existe"
        )
    return user

@router.get("/email", response_model=User)
async def get_user_by_email(
    email: EmailStr, 
    db: Session = Depends(get_session_db), 
    repository: PostgreSqlRepository = Depends(get_user_repository)
    ) -> User:
    user = repository.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El usuario con email {email} no existe"
        )
    return user

@router.post("/create")
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_session_db), 
    repository: PostgreSqlRepository = Depends(get_user_repository)
    ) -> str:
    new_user = repository.create_user(db, user_data)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al registrar el usuario {user_data.user_name}"
        )
    return f"✅ {user_data.user_name} te has registrado correctamente"

