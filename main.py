from fastapi import FastAPI

# Must be initialized first
app = FastAPI()

# These route imports must come after the app is created
from auth_routes import auth_router
from order_routes import order_router

# Register the authentication and order routers with the main app
# This makes their routes available in the FastAPI application
app.include_router(auth_router)
app.include_router(order_router)