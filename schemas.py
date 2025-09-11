from pydantic import BaseModel, EmailStr
from typing import Optional

# User Schemas
class SchemaUser(BaseModel):
    """
    Schema for creating and updating users.

    Attributes:
        name (str): Full name of the user.
        email (EmailStr): User email address (must be valid format).
        password (str): User password (hashed before persistence).
        active (Optional[bool]): Whether the user account is active.
        admin (Optional[bool]): Whether the user has administrative privileges.
    """
    name: str
    email: EmailStr
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy integration

# Order Schemas
class SchemaOrder(BaseModel):
    """
    Schema for creating a new order.

    Attributes:
        user_id (int): ID of the user who owns the order.
    """
    user_id: int

    class Config:
        from_attributes = True

# Authentication Schemas
class SchemaLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        email (EmailStr): User email address.
        password (str): User password (plain text, will be verified against hash).
    """
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

# Order Item Schemas
class OrderItemScheme(BaseModel):
    """
    Schema for creating an item inside an order.

    Attributes:
        quantity (int): Number of units for this item.
        taste (str): Flavor/type of the item (e.g., pizza flavor).
        size (str): Size of the item (e.g., small, medium, large).
        unit_price (float): Price per unit.
    """
    quantity: int
    taste: str
    size: str
    unit_price: float

    class Config:
        from_attributes = True