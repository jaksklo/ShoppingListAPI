from sqlalchemy.orm import Session
from app import models, schemas


# get user by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# get user by email
def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


# get list of all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# create a new user
def create_user(db: Session, user: schemas.UserCreate):
    fake_pwd_hash = "fake" + user.password
    db_user = models.User(email=user.email, name=user.name, password=fake_pwd_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # refresh your instance (so that it contains any new data from the database, like the generated ID)
    return db_user


# get single list
def get_list(db: Session, list_id: int):
    return db.query(models.List).filter(models.List.id == list_id).first()


# get all lists
def get_lists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.List).offset(skip).limit(limit).all()


# get all lists belonging to specific user
def get_user_lists(db: Session, user_id: int,  skip: int = 0, limit: int = 100):
    return db.query(models.List).filter(models.List.user_id == user_id).offset(skip).limit(limit).all()


# create a new list
def create_list(db: Session, prodlist: schemas.ShoppingListCreate, user_id: int):
    db_list = models.List(title=prodlist.title, user_id=user_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


# get single product
def get_product(db: Session, prod_id: int):
    return db.query(models.Product).filter(models.Product.id == prod_id).first()


# get all products from list
def get_list_products(db: Session, list_id: int):
    return db.query(models.Product).filter(models.Product.list_id == list_id).all()


# get all products
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


# create new product
def create_product(db: Session, product: schemas.ProductCreate, list_id: int):
    db_product = models.Product(name=product.name, quantity=product.quantity, list_id=list_id,
                                is_purchased=product.is_purchased)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
