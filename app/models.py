from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    lists = relationship("List", back_populates="owner")


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="lists")
    products = relationship("Product", back_populates="list")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete='CASCADE'))
    quantity = Column(Float, nullable= False)
    is_purchased = Column(Boolean, default=False)

    list = relationship("List", back_populates="products")
