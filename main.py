from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Secret key for authentication and security purposes
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Initialize the FastAPI application (must be created before routers are imported)
app = FastAPI()

# Import routers (must be done after app initialization)
from auth_routes import auth_router
from order_routes import order_router

# Register routers with the FastAPI application
# This makes authentication and order endpoints available
app.include_router(auth_router)
app.include_router(order_router)
