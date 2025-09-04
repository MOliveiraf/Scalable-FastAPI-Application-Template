from pydantic import BaseModel
from typing import Optional

class SchemaUser(BaseModel):
    """
    Schema for validating and serializing user data.
    Used when creating or updating users via API requests.
    """
    name: str                
    email: str               
    password: str            
    active: Optional[bool]   
    admin: Optional[bool]     

    class Config:
        # Enables compatibility with ORM models (SQLAlchemy)
        from_attributes = True
