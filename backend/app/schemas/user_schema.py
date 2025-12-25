from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    """Base user schema."""
    user_email: EmailStr
    user_name: str
    role: Optional[str] = "normal"  # "admin" or "normal"


class UserCreate(UserBase):
    """Schema for creating a user."""
    pwd: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    user_email: Optional[EmailStr] = None
    user_name: Optional[str] = None
    pwd: Optional[str] = None


class UserRead(UserBase):
    """Schema for reading a user."""
    id: str
    role: str

    model_config = ConfigDict(from_attributes=True)