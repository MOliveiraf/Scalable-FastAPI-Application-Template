from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# Cria a conexão do banco
db = create_engine("sqlite:///banco.db")

# Base declarativa para as tabelas
Base = declarative_base()


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)
    
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
    status = Column("status", String)
    user_id = Column("user", ForeignKey("users.id"))
    price = Column("price", Float)

    def __init__(self, user_id, status="PENDING", price=0):
        self.user_id = user_id
        self.status = status
        self.price = price


# OrderItem Model
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    taste = Column("taste", String)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order_id = Column("order", ForeignKey("orders.id"))      

    def __init__(self, quantity, taste, size, unit_price, order_id):
        self.quantity = quantity
        self.taste = taste
        self.size = size
        self.unit_price = unit_price
        self.order_id = order_id
