from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import SessionLocal, engine
from app import models, schemas
from app.auth import hash_password
from app.auth import verify_password, create_access_token
from app.auth import get_current_user
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# View User
@app.get("/users", response_model=List[schemas.UserResponse])
def get_users(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(models.User).all()

# Edit User
@app.put("/users/{user_id}")
def update_user(
    user_id: int, 
    user: schemas.UserCreate, 
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    db_user = db.query(models.User).filter(
        models.User.user_id == user_id
    ).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")

    db_user.name = user.name
    db_user.age = user.age
    db_user.department = user.department
    db_user.skills = user.skills
    db_user.role = user.role
    
    db.commit()
    db.refresh(db_user)

    return db_user

# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.user_id == user_id
    ).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")

    db.delete(db_user)
    db.commit()

    return {"message": "User Deleted Successfully"}

# Resgister User
@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # Username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    # Name cannot contain numbers
    if not user.name.replace(" ", "").isalpha():
        raise HTTPException(
            status_code=400,
            detail="Name should contain only alphabets."
        )

    new_user = models.User(
        name=user.name,
        age=user.age,
        username=user.username,
        password=hash_password(user.password),
        department=user.department,
        skills=user.skills,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully."
    }
# # bydefault page 
# @app.get("/")
# def home(db:Session = Depends(get_db)):
#     return {
#         "message": "Welcome to the FastAPI CRUD Application!"
#         }
         
# Login User
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }