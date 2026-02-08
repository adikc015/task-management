from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from models.department import Department

class Project(Base):
    __tablename__ = "projects"
    
    id=Column(Integer, primary_key=True)
    name=Column(String(150), nullable=False)
    
    department_id=Column(Integer, ForeignKey("departments.id"))
    department=relationship("Department",backref="projects")