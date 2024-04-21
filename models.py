from sqlalchemy import Column, String, Integer, Boolean, Text, Enum, ForeignKey
from schema.order import OrderStatus, PizzaSizes
from sqlalchemy.orm import relationship
from database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_staff": self.is_staff,
            "is_active": self.is_active,
        }
    

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    pizza_size = Column(Enum(PizzaSizes), default=PizzaSizes.small)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship('User', back_populates='orders')

    def serialize(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "order_status": self.order_status,
            "pizza_size": self.pizza_size,
            "user_id": self.user_id,
        }















