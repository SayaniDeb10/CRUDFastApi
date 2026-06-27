from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str 
    
class UserCreate(BaseModel):
    name: str
    age: int
    username: str
    password: str

class UserResponse(UserCreate):
    user_id: int
    name: str
    age: int
    username: str

    class Config:
        from_attributes = True