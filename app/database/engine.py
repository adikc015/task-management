from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

MY_SQL = "mysql+pymysql://root:Ghy%401234@localhost:3306"

engine=create_engine(MY_SQL, echo=True)

Database_name="task_management"

db_status=False

try:
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {Database_name}"))
        print(f"{Database_name} database created successfully.")
        db_status=True
except Exception as e:
    print("Operation failed: Could not initialize the database.", e)
    
    
if db_status==True:
    DATABASE_URL = f"mysql+pymysql://root:Ghy%401234@localhost:3306/{Database_name}"
    engine=create_engine(DATABASE_URL, echo=True)
    SessionLocal=sessionmaker(bind=engine)
    session=SessionLocal()
    print("Database created successfully, ready to work")
    session.close()
else:
    print("Unable to create database due to an internal error.")