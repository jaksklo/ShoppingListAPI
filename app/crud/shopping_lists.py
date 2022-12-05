from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app.schemas.shoppinglist import ShoppingListCreate


# get single list detailed view if belongs to user
def get_list(db: Session, list_id: int, user_id: int):
    list_db = db.query(models.List).filter(models.List.id == list_id).first()
    if list_db is None:
        raise HTTPException(status_code=404, detail="List not found")
    if list_db.user_id != user_id:
        raise HTTPException(status_code=404, detail="Selected list does not belong to this user")

    return list_db


# get all lists
def get_lists(db: Session, skip: int = 0, limit: int = 100):
    lists_db = db.query(models.List).offset(skip).limit(limit).all()
    for element in lists_db:
        element.product_count = len(element.products)
    return lists_db


# get all lists belonging to specific user
def get_user_lists(db: Session, user_id: int,  skip: int = 0, limit: int = 100):
    return db.query(models.List).filter(models.List.user_id == user_id).offset(skip).limit(limit).all()


# create a new list
def create_list(db: Session, prodlist: ShoppingListCreate, user_id: int):
    prodlist_data = prodlist.dict()
    prodlist_data['user_id'] = user_id
    prods_data = prodlist_data.pop('products')
    db_list = models.List(**prodlist_data)
    db.add(db_list)
    db.flush()
    list_id = db_list.id
    for product in prods_data:
        product['list_id'] = list_id
        db_product = models.Product(**product)
        db.add(db_product)
        db.flush()
    db.commit()
    return db_list


def update_list(list_id: str, db: Session, prodlist: ShoppingListCreate, user_id: str):
    prodlist_data = prodlist.dict()

    list_from_db = get_list(db, list_id, user_id)
    list_from_db.title = prodlist_data.pop("title")
    prods_data = prodlist_data.pop('products')

    db.add(list_from_db)
    db.flush()

    if len(prods_data) > 0:
        # remove old products
        db.query(models.Product).filter(models.Product.list_id == list_from_db.id).delete()

        for product in prods_data:
            product['list_id'] = list_id
            db_product = models.Product(**product)
            db.add(db_product)
            db.flush()
    db.commit()
    return list_from_db


def delete_list(list_id: str, db: Session, user_id: str):
    list_from_db = get_list(db, list_id, user_id)
    db.delete(list_from_db)
    db.commit()
    return successful_response(200)


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }
