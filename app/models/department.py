from database.base import Base
from sqlalchemy import String, Integer, Column

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)