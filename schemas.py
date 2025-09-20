from pydantic import BaseModel, EmailStr
from typing import Optional, List

# -----------------------------------------------------------------------------
# User Schemas
# -----------------------------------------------------------------------------
class SchemaUser(BaseModel):
    """
    Schema for creating and updating users.

    Attributes:
        name (str): Full name of the user.
        email (EmailStr): User email address (must follow a valid format).
        password (str): User password (stored as a hash in the database).
        active (Optional[bool]): Indicates if the account is active. Default: True.
        admin (Optional[bool]): Indicates if the user has admin privileges. Default: False.
    """
    name: str
    email: EmailStr
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy integration


# -----------------------------------------------------------------------------
# Order Schemas
# -----------------------------------------------------------------------------
class SchemaOrder(BaseModel):
    """
    Schema for creating a new order.

    Attributes:
        user_id (int): ID of the user who owns the order.
    """
    user_id: int

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Authentication Schemas
# -----------------------------------------------------------------------------
class SchemaLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        email (EmailStr): User email address.
        password (str): Plain text password (will be validated against hash).
    """
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Order Item Schemas
# -----------------------------------------------------------------------------
class SchemaOrderItem(BaseModel):
    """
    Schema for creating or representing an item inside an order.

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


# -----------------------------------------------------------------------------
# Order Response Schema
# -----------------------------------------------------------------------------
class SchemaOrderResponse(BaseModel):
    """
    Schema for representing an order response.

    Attributes:
        id (int): Unique ID of the order.
        status (str): Current status of the order (e.g., PENDING, FINISHED, CANCELED).
        price (float): Total price of the order.
        items (List[SchemaOrderItem]): List of items belonging to the order.
    """
    id: int
    status: str
    price: float
    items: List[SchemaOrderItem]

    class Config:
        from_attributes = True
