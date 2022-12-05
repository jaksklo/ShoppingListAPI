from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    quantity: float
    is_purchased: bool = False


class Product(ProductBase):
    id: str
    list_id: str

    class Config:
        orm_mode = True
