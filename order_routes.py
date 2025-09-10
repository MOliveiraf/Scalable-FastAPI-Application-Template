from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, token_verification
from schemas import SchemaOrder
from models import Order, User

# Router for order-related endpoints.
# All routes are prefixed with "/orders" and grouped under the "orders" tag.
# Authentication is enforced globally for this router.
order_router = APIRouter(
    prefix="/orders", 
    tags=["orders"], 
    dependencies=[Depends(token_verification)]
)


@order_router.get("/")
async def get_orders():
    """
    Health-check endpoint for the orders router.
    Returns a simple JSON message to confirm accessibility.
    """
    return {"message": "You have accessed the orders route"}


@order_router.post("/order")
async def post_orders(schema_order: SchemaOrder, session: Session = Depends(get_session)):
    """
    Create a new order for a given user.

    Args:
        schema_order (SchemaOrder): Payload containing the user ID.
        session (Session): Database session dependency.

    Returns:
        dict: Success message with the newly created order ID.
    """
    # Create a new order linked to the provided user ID
    new_order = Order(user_id=schema_order.user_id)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return {"message": f"Order created successfully. Order ID: {new_order.id}"}


@order_router.post("/order/cancel/{order_id}")
async def cancel_order(
    order_id: int, 
    session: Session = Depends(get_session), 
    user: User = Depends(token_verification)
):
    """
    Cancel an order by its ID.

    - Returns 400 if the order does not exist.
    - Only the order owner or an admin can cancel the order.
    - Updates the order status to 'CANCELED'.

    Args:
        order_id (int): The ID of the order to cancel.
        session (Session): Database session dependency.
        user (User): The currently authenticated user.

    Returns:
        dict: Confirmation message and the canceled order details.
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to cancel this order.")    

    order.status = "CANCELED"
    session.commit()

    return {
        "message": f"Order ID {order.id} was successfully canceled",
        "order": order
    }
