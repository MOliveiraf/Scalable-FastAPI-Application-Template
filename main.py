from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Import routers after app initialization
from auth_routes import auth_router
from order_routes import order_router

# Register routers
app.include_router(auth_router)
app.include_router(order_router)
