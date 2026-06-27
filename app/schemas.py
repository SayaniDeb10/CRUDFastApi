from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(UserCreate):
    user_id: int

    class Config:
        from_attributes = True