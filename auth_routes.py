from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, token_verification
from schemas import SchemaUser, SchemaLogin
from sqlalchemy.orm import Session
from security import bcrypt_context
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

# Router for authentication endpoints
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# JWT token generator
def token_create(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration  
    dic_info = {"sub": str(user_id), "exp": expiration_date}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)    
    return encoded_jwt

# Validate user credentials
def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user


@auth_router.get("/")
async def home():
    """Basic health-check endpoint for authentication service."""
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
    Authenticate user and return access + refresh tokens.
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


@auth_router.post("/login-form")
async def login_form(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):  
    """
    OAuth2-compatible login using form-data (Swagger UI support).
    """
    user = authenticate_user(data_form.username, data_form.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credentials")

    access_token = token_create(user.id)        
    return {
        "access_token": access_token,            
        "token_type": "Bearer"
    }


@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(token_verification)):
    """
    Generate a new access token from a valid refresh token.
    """
    access_token = token_create(user.id)    
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
