from pydantic import BaseModel
from typing import Optional


class SchemaUser(BaseModel):
    """Schema for user creation and updates."""
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        # Allow conversion from ORM objects (SQLAlchemy models)
        from_attributes = True


class SchemaOrder(BaseModel):
    """Schema for order creation."""
    user_id: int

    class Config:
        from_attributes = True


class SchemaLogin(BaseModel):
    """Schema for user login requests."""
    email: str
    password: str

    class Config:
        from_attributes = True
