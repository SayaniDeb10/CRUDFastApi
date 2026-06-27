from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(
        name=user.name,
        age=user.age
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Created Successfully",
        "user": new_user
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):

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
def delete_user(user_id: int, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.user_id == user_id
    ).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")

    db.delete(db_user)
    db.commit()

    return {"message": "User Deleted Successfully"}