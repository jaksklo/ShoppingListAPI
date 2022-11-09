import uvicorn
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/lists", response_model=schemas.ShoppingList)
def create_list(shopping_list: schemas.ShoppingListCreate, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Cannot create list for non-existing user")
    return crud.create_list(db, prodlist=shopping_list, user_id=user_id)

@app.get("/lists/", response_model=List[schemas.ShoppingList])
def read_lists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prod_lists = crud.get_lists(db, skip=skip, limit=limit)
    return prod_lists

@app.get("/lists/{user_id}", response_model=List[schemas.ShoppingList])
def read_user_lists(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Cannot display lists for non-existing user")
    prod_lists = crud.get_user_lists(db, user_id=user_id, skip=skip, limit=limit)
    return prod_lists
