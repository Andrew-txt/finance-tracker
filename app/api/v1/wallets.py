from sqlalchemy.orm import Session

from app.models import User
from app.schemas import CreateWalletRequest
from app.services import wallets as wallet_service
from fastapi import APIRouter, Depends
from app.dependency import get_db, get_current_user

router = APIRouter()

@router.get("/balance")
def get_balance(wallet_name: str | None = None, db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)):
    return wallet_service.get_balance(db, current_user, wallet_name)


@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    return wallet_service.create_wallet(db, current_user, wallet)