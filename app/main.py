import uvicorn
from fastapi import FastAPI
from app.models import models
from app.utils.database import engine
import app.routers.users as users
import app.routers.shopping_lists as shopping_lists
import app.routers.auth as auth
import app.routers.products as prod
from sqlalchemy.engine import Engine
from sqlalchemy import event

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


app.include_router(users.router)
app.include_router(shopping_lists.router)
app.include_router(auth.router)
app.include_router(prod.router)


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
