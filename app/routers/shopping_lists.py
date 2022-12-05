from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.utils.database import get_db
from typing import List
import app.crud.shopping_lists as crud_lists
from ..utils.authentication import get_current_active_user
from app.schemas.user import User
from app.schemas.shoppinglist import ShoppingList, ShoppingListCreate, ShoppingListinListView


router = APIRouter(prefix='/lists', tags=['shopping lists'])


@router.post("/", response_model=ShoppingList)
async def create_list(shopping_list: ShoppingListCreate, current_user: User = Depends(get_current_active_user),
                      db: Session = Depends(get_db)):
    # db_user = get_user(db, user_id=current_user.id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="Cannot create list for non-existing user")
    return crud_lists.create_list(db, prodlist=shopping_list, user_id=current_user.id)


@router.get("/", response_model=List[ShoppingListinListView])
async def read_all_lists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_active_user)):
    prod_lists = crud_lists.get_lists(db, skip=skip, limit=limit)
    return prod_lists


@router.get("/{list_id}", response_model=ShoppingList)
async def read_list_details(list_id: str, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_active_user)):
    # db_user = get_user(db, user_id=current_user.id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="Cannot display list for non-existing user")
    list_details = crud_lists.get_list(db=db, list_id=list_id, user_id=current_user.id)
    return list_details


@router.get("/{list_id}", response_model=ShoppingList)
async def read_list_details(list_id: str, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_active_user)):
    # db_user = get_user(db, user_id=current_user.id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="Cannot display list for non-existing user")
    list_details = crud_lists.get_list(db=db, list_id=list_id, user_id=current_user.id)
    return list_details


@router.put("/{list_id}", response_model=ShoppingList)
async def update_list(list_id: str, shopping_list: ShoppingListCreate,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    # db_user = get_user(db, user_id=current_user.id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="Cannot edit list for non-existing user")
    list_details = crud_lists.update_list(db=db, list_id=list_id, user_id=current_user.id, prodlist=shopping_list)
    return list_details


@router.delete("/{list_id}")
async def delete_list(list_id: str, current_user: User = Depends(get_current_active_user),
                      db: Session = Depends(get_db)):
    return crud_lists.delete_list(list_id=list_id, user_id=current_user.id, db=db)
