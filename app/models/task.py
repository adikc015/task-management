from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.base import Base
from models.project import Project
from models.user import User

task_user = Table(
    "task_user",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("user_id",ForeignKey("users.id"), primary_key=True)
)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")
    priority = Column(String(50))
    due_date = Column(Date)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", backref="tasks")

    assigned_users = relationship(
        "User",
        secondary=task_user,
        backref="tasks"
    )