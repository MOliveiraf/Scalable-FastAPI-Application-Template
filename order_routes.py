from fastapi import APIRouter

# Create a router for authentication-related endpoints
# All routes will be prefixed with "/auth" and tagged as "auth"
order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def get_orders():
    return {"message": "You have accessed orders route"}