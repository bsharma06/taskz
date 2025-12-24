from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)