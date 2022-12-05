from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models import models
from sqlalchemy import or_
from ..utils.authentication import get_password_hash
from app.schemas.user import UserBase, UserCreate, UserUpdate
import os

# get user by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# get user by email or nick
def get_user_by_email_or_nick(db: Session, user_schema: UserBase):
    return db.query(models.User) \
        .filter(or_(models.User.email == user_schema.email, models.User.username == user_schema.username)).first()


# get list of all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    db_result = db.query(models.User).offset(skip).limit(limit).all()
    for user in db_result:
        user.list_count = len(user.lists)
    return db_result


# create a new user
def create_user(db: Session, user_in: UserCreate):
    user_in_dict = user_in.dict()
    if user_in_dict.get("password") != user_in_dict.get("confirm_password"):
        raise password_exception()

    hashed_password = get_password_hash(user_in_dict.pop("password"))
    user_in_dict.pop("confirm_password")
    user_in_dict["hashed_password"] = hashed_password
    db_user = models.User(**user_in_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # refresh your instance (so that it contains any new data from the database, like the generated ID)
    return db_user


# get all products related to user's list
def get_user_products(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Product).join(models.List).join(models.User) \
        .filter(models.Product.list_id == models.List.id).filter(models.List.user_id == user_id).offset(skip).limit(
        limit).all()


# delete user by id
def delete_user(user_id: str, db: Session):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_model:
        raise http_not_found_exception()

    if user_model.profile_pic is not None:
        try:
            target = os.path.join(os.getcwd(), "media", "users", user_id, "profile.png")
            os.remove(target)
        except OSError:
            pass

    db.delete(user_model)
    db.commit()
    return successful_response(200)


# update user
def update_user(user_updates: UserUpdate, user_id: str, db: Session):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_model:
        raise http_not_found_exception()

    update_data = user_updates.dict(exclude_unset=True)

    # verify password matches
    if 'password' in update_data and 'confirm_password' in update_data:
        if update_data.get('password') == update_data.get("confirm_password"):
            hashed_password = get_password_hash(update_data.pop("password"))
            update_data.pop("confirm_password")
            update_data['hashed_password'] = hashed_password
        else:
            raise password_exception()
    elif ('password' in update_data and 'confirm_password' not in update_data) or (
            'password' not in update_data and 'confirm_password' in update_data):
        raise password_exception()

    for key, value in update_data.items():
        setattr(user_model, key, value) if value else None
    db.add(user_model)
    db.commit()

    return user_model


# upload user's image
async def upload_profile_pic(file: UploadFile, user_id: str, db: Session):
    target_dir = os.path.join(os.getcwd(), "media", "users", user_id)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    target_name = os.path.join(target_dir, "profile.png")
    with open(target_name, "wb+") as f:
        content = await file.read()
        f.write(content)
    db.query(models.User).filter(models.User.id == user_id).update({"profile_pic": target_name})
    db.commit()

    return successful_response(200)


# get user's image
def get_profile_pic(user_id: str, db: Session):
    profile_path = db.query(models.User.profile_pic).filter(models.User.id == user_id).first()
    if len(profile_path) > 0:
        profile_path = profile_path[0]
    else:
        profile_path = None

    if profile_path is None or not os.path.exists(profile_path):
        raise http_not_found_exception()
    else:
        return str(profile_path)


def password_exception():
    raise HTTPException(status_code=400, detail="Password mismatch")


def http_not_found_exception():
    raise HTTPException(status_code=404, detail="Object not found")


def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }
