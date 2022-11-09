import datetime
from typing import List
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    quantity: float


class ProductCreate(ProductBase):
    is_purchased: bool = False


class Product(BaseModel):
    id: int
    list_id: int
    is_purchased: bool

    class Config:
        orm_mode = True


class ShoppingListBase(BaseModel):
    title: str


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingList(ShoppingListBase):
    id: int
    user_id: int
    creation_date: datetime.datetime
    products: List[Product] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    lists: List[ShoppingList] = []

    class Config:
        orm_mode = True
