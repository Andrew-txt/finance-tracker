from fastapi import FastAPI
from fastapi import HTTPException
from app.database import Base, engine

from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operation_router

app = FastAPI()


app.include_router(wallet_router, prefix="/api/v1")
app.include_router(operation_router, prefix="/api/v1")

Base.metadata.create_all(bind=engine)