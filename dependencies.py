from fastapi import Depends, HTTPException
from config import SECRET_KEY, ALGORITHM
from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from security import oauth2_schema

# Provide a database session per request
def get_session():
    """
    Dependency that yields a database session.
    - Ensures each request has its own session.
    - Closes session automatically after use.
    """
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()  # Always close session


# Validate JWT token and return the authenticated user
def token_verification(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(get_session)
):
    """
    Token validation dependency.
    - Decodes JWT and extracts user ID.
    - Raises 401 if token is invalid or user not found.
    """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied, invalid token")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user

