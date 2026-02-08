# from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=False, index=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash=Column(String(256), nullable=False)
    role = Column(String(50), nullable=False)
    
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", backref="users")