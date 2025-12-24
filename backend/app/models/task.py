from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, index=True)
    start_date = Column(DateTime(timezone=True), index=True)
    due_date = Column(DateTime(timezone=True), index=True)
    priority = Column(String, index=True)
    status = Column(String, index=True)
    assigned_to = Column(String, ForeignKey("users.id"))
    tenant_id = Column(String, ForeignKey("tenants.id"))

    tenant = relationship("Tenant", backref="tasks")
    assigned_to_user = relationship("User", back_populates="tasks")

