from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, token_verification
from schemas import SchemaOrder, SchemaOrderItem', SchemaOrderResponse
from models import Order, User, OrderItem
from typing import List

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
    order_item_scheme: SchemaOrderItem',
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
        order_item_scheme (SchemaOrderItem'): Item payload (quantity, taste, size, unit_price).
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


@order_router.post("/order/remove-item/{order_item_id}")
async def remove_order_item(
    order_item_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(token_verification),
):   
    # Find the item
    order_item = session.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status_code=400, detail="Order item does not exist")

    # Get the parent order
    order = session.query(Order).filter(Order.id == order_item.order_id).first()

    # Authorization check
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401,
            detail="You are not authorized to remove items from this order."
        )

    # Remove item and update order price
    session.delete(order_item)
    order.price_calculate()
    session.commit()
    session.refresh(order)

    return {
        "message": "Item removed successfully",
        "quantity_order_item": len(order.items),
        "order": order
    }


# Complete an order
@order_router.post("/order/complete/{order_id}")
async def complete_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(token_verification),
):
    """
    Mark an order as completed by its ID.

    Rules:
    - Returns 400 if the order does not exist.
    - Only the order owner or an admin can complete it.
    - Updates the order status to 'COMPLETED'.
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401, 
            detail="You are not authorized to complete this order."
        )

    order.status = "COMPLETED"
    session.commit()

    return {
        "message": f"Order ID {order.id} was successfully completed",
        "order": order,
    }


# Get a single order
@order_router.get("/order/{order_id}")
async def get_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(token_verification),
):
    """
    Retrieve one order by its ID.

    Rules:
    - Returns 400 if the order does not exist.
    - Only the order owner or an admin can view it.
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401, 
            detail="You are not authorized to view this order."
        )

    return {
        "quantity_order_item": len(order.items),
        "order": order
    }

# List all orders for the authenticated user
@order_router.get("/orders/me", response_model=List[SchemaOrderResponse])
async def get_my_orders(
    session: Session = Depends(get_session), 
    user: User = Depends(token_verification)
):
    """
    Retrieve all orders belonging to the authenticated user.

    Args:
        session (Session): Database session dependency.
        user (User): Authenticated user.

    Returns:
        dict: A list of the user's own orders.
    """  
    orders = session.query(Order).filter(Order.user_id == user.id).all()
    return orders
