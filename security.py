from passlib.context import CryptContext

# Configure password hashing with bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
