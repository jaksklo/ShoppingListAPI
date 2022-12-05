from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
import app.crud.products as crud_products
from app.utils.database import get_db
from app.utils.authentication import get_current_active_user
from app.schemas.product import Product, ProductBase
from app.schemas.user import User

router = APIRouter(prefix='/products', tags=['products'])


@router.get("/{product_id}/", response_model=Product)
async def read_product_details(product_id: str, db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_active_user)):
    return crud_products.get_product(product_id=product_id, db=db, user_id=current_user.id)


@router.post("/", response_model=Product)
async def add_product(list_id: str, new_product: ProductBase, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    return crud_products.add_product(list_id=list_id, product_in=new_product, db=db, user_id=current_user.id)


@router.put("/{product_id}/", response_model=Product)
async def update_product(product_id: str, new_product: ProductBase, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_active_user)):
    return crud_products.update_product(product_id=product_id, product_in=new_product, db=db, user_id=current_user.id)


@router.post("/{product_id}/purchased", response_model=Product)
async def change_purchased_status(product_id: str, db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_active_user)):
    return crud_products.change_purchased_status(product_id=product_id, db=db, user_id=current_user.id)


@router.delete("/{product_id}/")
async def change_purchased_status(product_id: str, db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_active_user)):
    return crud_products.delete_product(product_id=product_id, db=db, user_id=current_user.id)
