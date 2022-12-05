import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.product import ProductBase, Product


class ShoppingListBase(BaseModel):
    title: str


class ShoppingListCreate(ShoppingListBase):
    products: List[ProductBase] | None = []


class ShoppingList(ShoppingListBase):
    id: str
    user_id: str
    creation_date: datetime.datetime
    products: List[Product] = []

    class Config:
        orm_mode = True


class ShoppingListinListView(ShoppingListBase):
    id: str
    product_count: int
    user_id: str

    class Config:
        orm_mode = True
