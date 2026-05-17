from exceptions import EmailAlreadyExistsError, UserDoesNotExistsError
from schemas import UserResponse, UserData, IdModel
from api.dependencies import get_user_repository
from core import IUserRepository

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def get_all(repository: IUserRepository = Depends(get_user_repository)) -> List[UserResponse]:
    return repository.get_all()

@router.get("/get/id", response_model=UserResponse)
async def get_user_by_id(id: IdModel, repository: IUserRepository = Depends(get_user_repository)) -> UserResponse:
    try:
        return repository.get_user_by_id(id)
    except UserDoesNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
@router.post("/create", response_model=UserResponse)
async def create(data: UserData, repository: IUserRepository = Depends(get_user_repository)) -> UserResponse:         
        try:
            return repository.create(data)
        except EmailAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )

@router.post("/create-many")
async def create_many(users: List[UserData], repository: IUserRepository = Depends(get_user_repository)):
    try:
        sucess =  repository.create_many(users)
        if sucess:
            return "Users successfully created"
    except EmailAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
           
@router.put("/update", response_model=UserResponse)
async def update(id: IdModel, data: UserData, repository: IUserRepository = Depends(get_user_repository)) -> UserResponse:
    try:
        return repository.update(id, data)
    except UserDoesNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/delete")        
async def delete(id: IdModel, repsotiory: IUserRepository = Depends(get_user_repository)):
    try:
        row_del = repsotiory.delete(id)
        if row_del:
            return "Successfully removed"
    except UserDoesNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )