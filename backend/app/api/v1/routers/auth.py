from backend.app.api.dependencies import get_user_repository, get_session_db, get_password_hasher
from backend.app.schemas import Token
from backend.app.crud import PostgreSqlRepository
from backend.app.core import PasswordHasher, create_access_token

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session_db),
    repository: PostgreSqlRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher)
):
    user = repository.get_user(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not hasher.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session_db),
    repository: PostgreSqlRepository = Depends(get_user_repository)
):
    from backend.app.schemas import UserCreate
    
    existing_user = repository.get_user(db, form_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario {form_data.username} ya existe"
        )
    
    user_data = UserCreate(
        user_name=form_data.username,
        email=f"{form_data.username}@temp.com",
        password=form_data.password
    )
    repository.create_user(db, user_data)
    return {"message": f"✅ Usuario {form_data.username} registrado correctamente"}