from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, token_verification
from schemas import SchemaOrder, OrderItemScheme
from models import Order, User, OrderItem

# ---------------------------------------------------------------------------- 
# Orders Router
# ---------------------------------------------------------------------------- 
# - All routes are prefixed with "/orders".
# - All routes require authentication via `token_verification`.
# - Provides endpoints for managing orders and their items.
# ---------------------------------------------------------------------------- 
order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(token_verification)]
)

# Health-check endpoint
@order_router.get("/")
async def get_orders():
    """
    Health-check endpoint for the orders router.

    Returns:
        dict: A simple message confirming that the orders route is accessible.
    """
    return {"message": "You have accessed the orders route"}

# Create a new order
@order_router.post("/order")
async def post_orders(schema_order: SchemaOrder, session: Session = Depends(get_session)):
    """
    Create a new order linked to a specific user.

    Args:
        schema_order (SchemaOrder): Payload containing the user ID.
        session (Session): Database session dependency.

    Returns:
        dict: Success message with the created order ID.
    """
    new_order = Order(user_id=schema_order.user_id)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return {"message": f"Order created successfully. Order ID: {new_order.id}"}

# Cancel an order
@order_router.post("/order/cancel/{order_id}")
async def cancel_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(token_verification),
):
    """
    Cancel an order by its ID.

    Rules:
    - Returns 400 if the order does not exist.
    - Only the order owner or an admin can cancel it.
    - Updates the order status to 'CANCELED'.

    Args:
        order_id (int): Order ID to cancel.
        session (Session): Database session dependency.
        user (User): Authenticated user.

    Returns:
        dict: Confirmation message and canceled order details.
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401, 
            detail="You are not authorized to cancel this order."
        )

    order.status = "CANCELED"
    session.commit()

    return {
        "message": f"Order ID {order.id} was successfully canceled",
        "order": order,
    }

# List all orders (Admin only)
@order_router.get("/list")
async def order_list(
    session: Session = Depends(get_session), 
    user: User = Depends(token_verification)
):
    """
    Retrieve all orders (Admin only).

    Args:
        session (Session): Database session dependency.
        user (User): Authenticated user.

    Returns:
        dict: A list of all orders if user is admin.
    """
    if not user.admin:
        raise HTTPException(
            status_code=401,
            detail="You are not authorized to perform this operation."
        )

    orders = session.query(Order).all()
    return {"orders": orders}

# Add an item to an order
@order_router.post("/order/item-add/{order_id}")
async def add_order_item(
    order_id: int,
    order_item_scheme: OrderItemScheme,
    session: Session = Depends(get_session),
    user: User = Depends(token_verification),
):
    """
    Add a new item to an existing order.

    Rules:
    - The order must exist.
    - Only the order owner or an admin can add items.
    - Automatically recalculates the total order price.

    Args:
        order_id (int): ID of the order to update.
        order_item_scheme (OrderItemScheme): Item payload (quantity, taste, size, unit_price).
        session (Session): Database session dependency.
        user (User): Authenticated user.

    Returns:
        dict: Confirmation message, item details, and updated order total.
    """
    # Validate order existence
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order does not exist")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401,
            detail="You are not authorized to add items to this order."
        )

    # Create and attach item
    order_item = OrderItem(
        order_item_scheme.quantity,
        order_item_scheme.taste,
        order_item_scheme.size,
        order_item_scheme.unit_price,
        order_id,
    )
    session.add(order_item)
    session.flush()  # ensures the item is visible in order.items

    # Update total order price
    order.price_calculate()
    session.commit()
    session.refresh(order)

    return {
        "message": "Item created successfully",
        "order_item": {
            "id": order_item.id,
            "quantity": order_item.quantity,
            "unit_price": order_item.unit_price,
            "subtotal": order_item.unit_price * order_item.quantity,
        },
        "order_total": order.price,
    }
