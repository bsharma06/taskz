from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)    
    user_email = Column(String, unique=True, index=True)
    user_name = Column(String, index=True)
    pwd = Column(String, index=True)    
    tasks = relationship("Task", back_populates="assigned_to_user")

