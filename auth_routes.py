from fastapi import APIRouter

# Create a router for authentication-related endpoints
# All routes will be prefixed with "/auth" and tagged as "auth"
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def get_auth():
    """
    This is our system´s standard authentication routes
    
    """
    return {"message": "You have accessed the authentication route"}