from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from schemas import SchemaUser, SchemaLogin
from sqlalchemy.orm import Session
from security import bcrypt_context
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

# Router for authentication endpoints
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Simple token generator (placeholder, not secure for production)
def token_create(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration  
    dic_info = {"sub": user_id, "exp": expiration_date}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)    
    return encoded_jwt

def token_verification(token, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id==1).first()
    return user

def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user


@auth_router.get("/")
async def home():
    """Health-check route for authentication."""
    return {"message": "You have accessed the authentication route"}


@auth_router.post("/create_account")
async def create_account(schema_user: SchemaUser, session: Session = Depends(get_session)):
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
async def login(schema_login: SchemaLogin, session: Session = Depends(get_session)):
    """
    Authenticate a user and return an access token.
    - Validates email.
    - Generates a fake JWT token (placeholder).
    """
    user = authenticate_user(schema_login.email, schema_login.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credentials")

    access_token = token_create(user.id)
    refresh_token = token_create(user.id, token_duration=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.get("/refresh")
async def use_refresh_token(token):
    user = token_verification(token)
    access_token = token_create(user.id)    
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

