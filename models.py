from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

# Create database connection
db = create_engine("sqlite:///banco.db")

# Base for models
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


# Order Model
class Order(Base):
    __tablename__ = "orders"  

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="PENDING")
    user_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float, default=0.0)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

    def __init__(self, user_id, status="PENDING", price=0.0):
        self.user_id = user_id
        self.status = status
        self.price = price


# OrderItem Model
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    taste = Column(String)
    size = Column(String)
    unit_price = Column(Float)
    order_id = Column(Integer, ForeignKey("orders.id"))      

    order = relationship("Order", back_populates="items")

    def __init__(self, quantity, taste, size, unit_price, order_id):
        self.quantity = quantity
        self.taste = taste
        self.size = size
        self.unit_price = unit_price
        self.order_id = order_id
