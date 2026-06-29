from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    username = Column(String(100), unique=True)
    password = Column(String(255)),
    department = Column(String(100)),
    role = Column(String(50)),
    skills = Column(String(255))