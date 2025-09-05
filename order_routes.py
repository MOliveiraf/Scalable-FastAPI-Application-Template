from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_section
from schemas import SchemaOrder
from models import Order

# Router dedicated to order-related endpoints.
# All routes here will be prefixed with "/orders" and grouped under the "orders" tag.
order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def get_orders():
    """
    Root endpoint for order routes.
    Provides a simple response to confirm accessibility.
    """
    return {"message": "You have accessed the orders route"}


@order_router.post("/order")
async def post_orders(schema_order: SchemaOrder, session: Session = Depends(get_section)):
    """
    Endpoint to create a new order.
    - Receives the user ID via SchemaOrder.
    - Persists the new order in the database.
    """
    # Create new order linked to a user
    new_order = Order(user_id=schema_order.user_id)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return {"message": f"Order created successfully. Order ID: {new_order.id}"}
