from pydantic import BaseModel,Field, EmailStr,field_validator,ConfigDict
from typing import Literal

class Login(BaseModel):
    username: str
    password: str 


class UserCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    username: EmailStr
    password: str = Field(..., min_length=6, max_length=12)
    department: str
    skills: str
    role: Literal["Admin","Student"] # Literal -> Only these values are accepted

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value.strip().lower() in ["string", "test", "admin"]:
            raise ValueError("Please enter a valid name.")
        return value.title()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value.lower() == "string":
            raise ValueError("Please enter a valid password.")
        return value
    
class UserResponse(BaseModel):
    user_id: int
    name: str
    age: int
    username: str
    department: str
    role: str
    skills: str

    model_config = ConfigDict(from_attributes=True)