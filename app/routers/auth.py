from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from ..utils.authentication import authenticate_user, create_access_token, credentials_exception
from datetime import timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from app.utils.database import get_db

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/token")
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise credentials_exception
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    return {"access_token": token, "token_type": "bearer"}
