from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_section
from main import bcrypt_context
from schemas import SchemaUser
from sqlalchemy.orm import Session

# Router dedicated to authentication-related endpoints.
# All routes here will be prefixed with "/auth" and grouped under the "auth" tag.
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    """
    Root endpoint for authentication routes.
    Provides a simple response to confirm accessibility.
    """
    return {"message": "You have accessed the authentication route"}


@auth_router.post("/create_account")
async def create_account(schema_user: SchemaUser, session: Session = Depends(get_section)):
    """
    Endpoint to create a new user account.
    - Verifies if a user with the given email already exists.
    - Hashes the password before saving.
    - Persists the user in the database.
    """
    # Verify if the email is already registered
    user = session.query(User).filter(User.email == schema_user.email).first()
    if user:
        raise HTTPException(status_code=400, detail="A user already exists with this email address")

    # Hash the provided password
    hashed_password = bcrypt_context.hash(schema_user.password)

    # Create a new User instance with hashed password
    new_user = User(
        schema_user.name,
        schema_user.email,
        hashed_password,
        schema_user.active,
        schema_user.admin
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": f"User registered successfully: {schema_user.email}"}
