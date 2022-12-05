from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app.schemas.product import ProductBase


# get existing product if belongs to current user
def get_product(product_id: str, db: Session, user_id: str):
    product_model = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    if product_model.list.user_id == user_id:
        return product_model
    else:
        raise HTTPException(status_code=403, detail="Operation forbidden")


# add new product
def add_product(list_id: str, product_in: ProductBase, db: Session, user_id: str):
    list_model = db.query(models.List).filter(models.List.id == list_id).filter(models.User.id == user_id).first()
    if list_model is None:
        raise HTTPException(status_code=404, detail="List not found")
    product_model = models.Product(**product_in.dict(), list_id=list_id)
    db.add(product_model)
    db.commit()
    return product_model


# update existing product
def update_product(product_in: ProductBase, product_id: str, user_id: str, db: Session):
    product_model = get_product(product_id, db, user_id)
    data_in = product_in.dict()
    for key, value in data_in.items():
        if hasattr(product_model, key):
            setattr(product_model, key, value)
    db.commit()
    return product_model


# change purchased status
def change_purchased_status(product_id: str, db: Session, user_id: str):
    product_model = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    if product_model.list.user_id == user_id:
        product_model.is_purchased = not product_model.is_purchased
        db.add(product_model)
        db.commit()
        return product_model
    else:
        raise HTTPException(status_code=403, detail="Operation forbidden")


def delete_product(product_id: str, db: Session, user_id: str):
    product_model = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    if product_model.list.user_id == user_id:
        db.delete(product_model)
        return successful_response(200)
    else:
        raise HTTPException(status_code=403, detail="Operation forbidden")


def http_exception():
    raise HTTPException(status_code=404, detail="Object not found")


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }
