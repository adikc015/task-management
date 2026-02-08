from database.engine import engine
from database.base import Base

# IMPORTANT: import models so Base knows them
from models.user import User
from models.task import Task
from models.department import Department
from models.project import Project

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
