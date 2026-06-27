from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SERVER = "DESKTOP-PK86VSS"
DATABASE = "FastApiDB"

DATABASE_URL = (
    f"mssql+pyodbc://{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()