from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)