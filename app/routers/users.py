from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
import app.crud.users as crud_user
import app.crud.shopping_lists as crud_lists
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from typing import List
from ..utils.authentication import get_current_active_user
from app.schemas.user import User, UserCreate, UserInListView, UserUpdate
from app.schemas.product import Product
from app.schemas.shoppinglist import ShoppingList

router = APIRouter(prefix='/users', tags=['user'])


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email_or_nick(db, user_schema=user)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud_user.create_user(db=db, user_in=user)


@router.get("/", response_model=List[UserInListView])
async def list_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_active_user)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.patch("/me", response_model=User)
async def update_user_me(user_updates: UserUpdate, current_user: User = Depends(get_current_active_user),
                         db: Session = Depends(get_db)):
    user = crud_user.update_user(user_updates=user_updates, user_id=current_user.id, db=db)
    return user


@router.delete("/me")
async def delete_user_me(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):

    return crud_user.delete_user(user_id=current_user.id, db=db)


@router.get("/me/products", response_model=List[Product])
async def read_user_me_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                                current_user: User = Depends(get_current_active_user)):
    products = crud_user.get_user_products(db, user_id=current_user.id, skip=skip, limit=limit)
    return products


@router.get("/me/lists", response_model=List[ShoppingList], response_model_exclude={"user_id"})
async def read_user_me_lists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_active_user)):
    db_user = crud_user.get_user(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Cannot display lists for non-existing user")
    prod_lists = crud_lists.get_user_lists(db, user_id=current_user.id, skip=skip, limit=limit)
    return prod_lists


@router.post("/me/profilepic/")
async def send_profile_picture(file: UploadFile, current_user: User = Depends(get_current_active_user),
                               db: Session = Depends(get_db)):
    return await crud_user.upload_profile_pic(file, current_user.id, db)


@router.get("/me/profilepic/", response_class=FileResponse)
async def get_profile_picture(current_user: User = Depends(get_current_active_user),
                               db: Session = Depends(get_db)):

    return crud_user.get_profile_pic(current_user.id, db)
