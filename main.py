from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Secret key for authentication and security purposes
SECRET_KEY = os.getenv("SECRET_KEY")

# Initialize the FastAPI application (must be created before routers are imported)
app = FastAPI()

# Configure password hashing with bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Import routers (must be done after app initialization)
from auth_routes import auth_router
from order_routes import order_router

# Register routers with the FastAPI application
# This makes authentication and order endpoints available
app.include_router(auth_router)
app.include_router(order_router)
