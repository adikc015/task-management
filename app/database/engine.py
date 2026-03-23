from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings

MY_SQL = settings.DB_SERVER_URI

engine = create_engine(MY_SQL, echo=settings.DB_ENGINE_ECHO)

Database_name = settings.DB_NAME

db_status=False

try:
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {Database_name}"))
        print(f"{Database_name} database created successfully.")
        db_status=True
except Exception as e:
    print("Operation failed: Could not initialize the database.", e)
    
    
if db_status==True:
    DATABASE_URL = settings.DATABASE_URL or f"{MY_SQL}/{Database_name}"
    engine = create_engine(DATABASE_URL, echo=settings.DB_ENGINE_ECHO)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    print("Database created successfully, ready to work")
    session.close()
else:
    print("Unable to create database due to an internal error.")