from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import SessionLocal, engine
from app import models, schemas
from app.auth import hash_password
from app.auth import verify_password, create_access_token

from app.auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post("/users")
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     new_user = models.User(
#         name=user.name,
#         age=user.age
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {
#         "message": "User Created Successfully",
#         "user": new_user
#     }


# @app.get("/users")
# def get_users(db: Session = Depends(get_db)):
#     return db.query(models.User).all()

@app.get("/users")
def get_users(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(models.User).all()


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

    db.commit()
    db.refresh(db_user)

    return db_user


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

#Auth Resgister
@app.post("/register")
def register(user: schemas.UserCreate,
             db: Session = Depends(get_db)):

    # Check username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        name=user.name,
        age=user.age,
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully"
    }


# @app.post("/login")
# def login(user: schemas.Login,
#           db: Session = Depends(get_db)):

#     db_user = db.query(models.User).filter(
#         models.User.username == user.username
#     ).first()

#     if db_user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid Username or Password"
#         )

#     if not verify_password(user.password, db_user.password):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid Username or Password"
#         )

#     token = create_access_token(
#         {
#             "sub": db_user.username
#         }
#     )

#     return {
#         "access_token": token,
#         "token_type": "Bearer"
#     }
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