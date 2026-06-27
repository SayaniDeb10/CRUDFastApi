from pydantic import BaseModel,Field, EmailStr,field_validator

class Login(BaseModel):
    username: str
    password: str 


class UserCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    username: EmailStr
    password: str = Field(..., min_length=6, max_length=12)

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
    
# class UserCreate(BaseModel):
#     name: str = Field(..., min_length=4, max_length=50)
#     age: int = Field(..., gt= 0, lt = 120)
#     username: EmailStr
#     password: str = Field(...,min_length = 6 , max_length = 12)




# class UserCreate(BaseModel):
#     name: str
#     age: int
#     username: EmailStr
#     password: str

#     @field_validator("name")
#     @classmethod
#     def validate_name(cls, value):
#         if value.strip().lower() == "string":
#             raise ValueError("Please enter a valid name.")
#         return value

#     @field_validator("age")
#     @classmethod
#     def validate_age(cls, value):
#         if value <= 0:
#             raise ValueError("Age must be greater than 0.")
#         return value

#     @field_validator("password")
#     @classmethod
#     def validate_password(cls, value):
#         if value.strip().lower() == "string":
#             raise ValueError("Please enter a valid password.")
#         if len(value) < 8:
#             raise ValueError("Password must be at least 8 characters.")
#         return value

class UserResponse(UserCreate):
    user_id: int
    name: str
    age: int
    username: str

    class Config:
        from_attributes = True