from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_section
from main import bcrypt_context
from schemas import SchemaUser, SchemaLogin
from sqlalchemy.orm import Session

# Router for authentication endpoints
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Simple token generator (placeholder, not secure for production)
def token_create(user_id):
    token = f"kjashdahsh{user_id}"
    return token


@auth_router.get("/")
async def home():
    """Health-check route for authentication."""
    return {"message": "You have accessed the authentication route"}


@auth_router.post("/create_account")
async def create_account(schema_user: SchemaUser, session: Session = Depends(get_section)):
    """
    Register a new user.
    - Rejects if email already exists.
    - Hashes password before saving.
    """
    user = session.query(User).filter(User.email == schema_user.email).first()
    if user:
        raise HTTPException(status_code=400, detail="A user already exists with this email address")

    hashed_password = bcrypt_context.hash(schema_user.password)

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


@auth_router.post("/login")
async def login(schema_login: SchemaLogin, session: Session = Depends(get_section)):
    """
    Authenticate a user and return an access token.
    - Validates email.
    - Generates a fake JWT token (placeholder).
    """
    user = session.query(User).filter(User.email == schema_login.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    access_token = token_create(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
