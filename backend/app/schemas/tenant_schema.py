from pydantic import BaseModel, ConfigDict


class TenantBase(BaseModel):
    """Base tenant schema."""
    name: str


class TenantCreate(TenantBase):
    """Schema for creating a tenant."""
    pass


class TenantRead(TenantBase):
    """Schema for reading a tenant."""
    id: str

    model_config = ConfigDict(from_attributes=True)