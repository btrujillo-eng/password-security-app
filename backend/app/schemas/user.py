from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr = Field(min_length=10, max_length=255, description="User's email")
    user_name: str = Field(min_length=8, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$", description="User's name")
    
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    
class UserCreate(UserBase):
    password_hash: str = Field(min_length=8, max_length=128)
    
class UserLoggin(BaseModel):
    email_or_username: str = Field(min_length=8, max_length=128)
    password_hash: str = Field(min_length=8, max_length=128)
    
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    
class UserResponse(UserBase):
    id: int = Field(gt=0, description="User's id")
    created_at: datetime = Field(description="Exact date the account was created")
    modified_at: datetime = Field(description="Exact date the account was modified")
    
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)