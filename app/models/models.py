from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from app.utils.database import Base
from sqlalchemy.sql import func
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    username = Column(String, index=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    profile_pic = Column(String, nullable=True)
    rating = Column(Integer, default=3)

    lists = relationship("List", back_populates="owner", passive_deletes=True)


class List(Base):
    __tablename__ = "lists"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="lists")
    products = relationship("Product", back_populates="list", passive_deletes=True)


class Product(Base):
    __tablename__ = 'products'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String, index=True)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete='CASCADE'), nullable=False)
    quantity = Column(Float, nullable= False)
    is_purchased = Column(Boolean, default=False)

    list = relationship("List", back_populates="products")
