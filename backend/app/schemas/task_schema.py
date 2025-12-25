from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Base task schema."""
    title: str
    description: Optional[str] = None
    start_date: datetime
    due_date: datetime
    priority: str
    status: str


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    created_by: str
    assigned_to: str


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None


class TaskRead(TaskBase):
    """Schema for reading a task."""
    id: str
    created_by: str
    assigned_to: str

    model_config = ConfigDict(from_attributes=True)