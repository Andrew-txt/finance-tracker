from fastapi import FastAPI
from fastapi import HTTPException
from app.database import Base, engine
# from fastapi.staticfiles import StaticFiles

from app.api.v1.wallets import router as wallets_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router

app = FastAPI()

app.include_router(wallets_router, prefix="/api/v1")
app.include_router(operations_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

# app.mount("/static", StaticFiles(directory="app/static"), name="static") for static files in app
# http://127.0.0.1:8000/static/index.html

Base.metadata.create_all(bind=engine)