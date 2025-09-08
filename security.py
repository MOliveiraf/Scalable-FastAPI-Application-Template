from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# Password hashing configuration (using bcrypt)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication (login via form)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
