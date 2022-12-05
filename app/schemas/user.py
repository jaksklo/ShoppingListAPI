from pydantic import BaseModel, Field, EmailStr
from typing import List
from app.schemas.shoppinglist import ShoppingList


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=30)
    confirm_password: str = Field(min_length=4, max_length=30)


class User(UserBase):
    id: str
    is_active: bool = True
    lists: List[ShoppingList] = []

    class Config:
        orm_mode = True


class UserInListView(UserBase):
    id: str
    list_count: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    password: str | None = Field(min_length=4, max_length=30)
    confirm_password: str | None = Field(min_length=4, max_length=30)
    first_name: str | None = Field(min_length=1, max_length=50)
    last_name: str | None = Field(min_length=1, max_length=50)
