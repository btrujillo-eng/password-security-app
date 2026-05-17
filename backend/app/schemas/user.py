from pydantic import BaseModel, Field, EmailStr

class IdModel(BaseModel):
    id: int = Field(gt=0, description="User's id")


class UserData(BaseModel):
    name: str = Field(min_length=3, max_length=120, description="User's name")
    email: EmailStr = Field(description="User's email")
    
class UserResponse(BaseModel):
    id: int = Field(description="User's id")
    name: str = Field(min_length=3, max_length=120, description="User's name")
    email: EmailStr = Field(description="User's email")