from app.schemas import CreateWalletRequest
from app.services import wallets as wallet_service
from fastapi import APIRouter



router = APIRouter()


@router.get("/balance")
def get_balance(wallet_name: str | None = None):
    return wallet_service.get_balance(wallet_name)


@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    return wallet_service.create_wallet(wallet)