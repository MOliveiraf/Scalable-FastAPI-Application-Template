from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

# Create database connection (SQLite in this case)
db = create_engine("sqlite:///banco.db")

# Base class for all models
Base = declarative_base()


# ========================
# User Model
# ========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)  # Must be unique for authentication
    password = Column(String)
    active = Column(Boolean, default=True)               # Marks if the user is active
    admin = Column(Boolean, default=False)               # Marks if the user has admin privileges

    # Relationship: One user can have many orders
    orders = relationship("Order", back_populates="user")

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


# ========================
# Order Model
# ========================
class Order(Base):
    __tablename__ = "orders"  

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="PENDING")            # Order status (PENDING, CANCELED, etc.)
    user_id = Column(Integer, ForeignKey("users.id"))     # Link to the user who owns the order
    price = Column(Float, default=0.0)                    # Total price of the order

    # Relationship: One order belongs to one user
    user = relationship("User", back_populates="orders")

    # Relationship: One order can have many items
    items = relationship("OrderItem", cascade="all, delete")

    def __init__(self, user_id, status="PENDING", price=0.0):
        self.user_id = user_id
        self.status = status
        self.price = price

    def price_calculate(self):
        """
        Recalculate the order's total price
        based on the sum of all related order items.
        """
        self.price = sum(item.total_price for item in self.items)


# ========================
# OrderItem Model
# ========================
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)                            # Number of units of the item
    taste = Column(String)                                # Example: "CHEESE", "PEPPERONI"
    size = Column(String)                                 # Example: "SMALL", "LARGE"
    unit_price = Column(Float)                            # Price per single unit
    order_id = Column(Integer, ForeignKey("orders.id"))   # Link to the parent order      

    # Relationship: Each item belongs to a single order
    order = relationship("Order", back_populates="items")

    def __init__(self, quantity, taste, size, unit_price, order_id):
        self.quantity = quantity
        self.taste = taste
        self.size = size
        self.unit_price = unit_price  # Store the unit price, not multiplied
        self.order_id = order_id

    @property
    def total_price(self) -> float:
        """
        Return the total price for this item:
        unit price × quantity.
        """
        return self.unit_price * self.quantity
